"""
Authentication views for RequestBin
Handles login, logout, registration, user management, and OTP email verification
"""

from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from requestbin import app, auth_db, config
from requestbin.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from requestbin.auth.utils import send_otp_email, send_approval_notification
from functools import wraps


def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function


def approved_required(f):
    """Decorator to require approved user"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_approved:
            flash('Your account is pending approval. Please wait for an administrator to approve your registration.', 'warning')
            return redirect(url_for('auth.profile'))
        return f(*args, **kwargs)
    return decorated_function


@app.endpoint('auth.login')
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_db.get_user(form.email.data)
        if user and user.check_password(form.password.data):
            # Step 1: Check email verification (all users must verify email first)
            if not user.email_verified:
                flash('Please verify your email address first. Check your email for the OTP code.', 'warning')
                session['pending_email'] = user.email
                return redirect(url_for('auth.verify_email'))
            
            # Step 2: Check admin approval (for non-auto-approved domains)
            if not user.is_approved:
                flash('Your email is verified. Your account is now pending admin approval. '
                      'You will receive an email once approved.', 'info')
                return redirect(url_for('auth.login'))
            
            # Step 3: All checks passed - login successful
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.email}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)


@app.endpoint('auth.logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))


@app.endpoint('auth.register')
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = auth_db.create_user(
                email=form.email.data,
                password=form.password.data,
                is_admin=False
            )
            
            # All non-admin users require email verification via OTP
            if not user.is_admin and user.otp_code:
                # Send OTP email
                send_otp_email(user.email, user.otp_code)
                session['pending_email'] = user.email
                
                # Different messages based on auto-approval status
                if user.is_approved:
                    # Auto-approved domain - only needs email verification
                    flash(f'Registration successful! An OTP has been sent to {user.email}. '
                          f'Your domain is pre-approved - just verify your email to access RequestBin.', 'success')
                else:
                    # Non-auto-approved - needs email verification AND admin approval
                    flash(f'Registration successful! An OTP has been sent to {user.email}. '
                          f'Please verify your email first. After verification, an admin will review your registration.', 'info')
                
                return redirect(url_for('auth.verify_email'))
            else:
                # Admin user (shouldn't normally happen via registration)
                flash(f'Registration successful! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            
        except ValueError as e:
            flash(str(e), 'danger')
    
    auto_approve_domains = ', '.join(config.AUTO_APPROVE_DOMAINS)
    return render_template('auth/register.html', form=form, auto_approve_domains=auto_approve_domains)


@app.endpoint('auth.profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)


@app.endpoint('auth.admin_users')
@admin_required
def admin_users():
    """Admin page to manage users"""
    all_users = auth_db.get_all_users()
    pending_users = auth_db.get_pending_users()
    
    return render_template(
        'auth/admin_users.html',
        all_users=all_users,
        pending_users=pending_users
    )


@app.endpoint('auth.approve_user')
@admin_required
def approve_user(email):
    """Approve a pending user"""
    user = auth_db.get_user(email)
    
    if not user:
        flash(f'User {email} not found.', 'danger')
        return redirect(url_for('auth.admin_users'))
    
    # Check if email is verified before allowing approval
    if not user.email_verified:
        flash(f'Cannot approve {email}. User must verify their email address first.', 'warning')
        return redirect(url_for('auth.admin_users'))
    
    auth_db.approve_user(email)
    send_approval_notification(email)
    flash(f'User {email} has been approved.', 'success')
    return redirect(url_for('auth.admin_users'))


@app.endpoint('auth.reject_user')
@admin_required
def reject_user(email):
    """Reject a pending user"""
    if email == config.ADMIN_EMAIL:
        flash('Cannot delete the admin user.', 'danger')
    else:
        auth_db.reject_user(email)
        flash(f'User {email} has been rejected and removed.', 'success')
    return redirect(url_for('auth.admin_users'))


@app.endpoint('auth.verify_email')
def verify_email():
    """Email verification page with OTP"""
    # Get email from session
    email = session.get('pending_email')
    if not email:
        flash('No pending email verification found.', 'warning')
        return redirect(url_for('auth.register'))
    
    user = auth_db.get_user(email)
    if not user:
        flash('User not found.', 'danger')
        session.pop('pending_email', None)
        return redirect(url_for('auth.register'))
    
    # Check if already verified
    if user.email_verified:
        flash('Email already verified. You can now log in.', 'success')
        session.pop('pending_email', None)
        return redirect(url_for('auth.login'))
    
    # Handle OTP submission
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if user.verify_otp(otp):
            # OTP verified successfully
            auth_db.update_user(user)
            session.pop('pending_email', None)
            flash('Email verified successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            if not user.is_otp_valid():
                flash('OTP has expired. Please request a new one.', 'danger')
            else:
                flash('Invalid OTP code. Please try again.', 'danger')
    
    # Calculate time remaining
    expiry_seconds = user.get_otp_expiry_time()
    expiry_hours = int(expiry_seconds // 3600)
    expiry_minutes = int((expiry_seconds % 3600) // 60)
    
    return render_template('auth/verify_email.html', 
                         email=email, 
                         expiry_hours=expiry_hours,
                         expiry_minutes=expiry_minutes,
                         otp_valid=user.is_otp_valid())


@app.endpoint('auth.resend_otp')
def resend_otp():
    """Resend OTP code"""
    email = session.get('pending_email')
    if not email:
        flash('No pending email verification found.', 'warning')
        return redirect(url_for('auth.register'))
    
    user = auth_db.get_user(email)
    if not user:
        flash('User not found.', 'danger')
        session.pop('pending_email', None)
        return redirect(url_for('auth.register'))
    
    # Check if already verified
    if user.email_verified:
        flash('Email already verified. You can now log in.', 'success')
        session.pop('pending_email', None)
        return redirect(url_for('auth.login'))
    
    # Generate new OTP
    user.generate_otp()
    auth_db.update_user(user)
    
    # Send email
    send_otp_email(user.email, user.otp_code)
    
    flash('A new OTP code has been sent to your email.', 'success')
    return redirect(url_for('auth.verify_email'))


@app.endpoint('auth.change_password')
@login_required
def change_password():
    """Change password for logged-in user"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return render_template('auth/change_password.html', form=form)
        
        # Update password
        current_user.set_password(form.new_password.data)
        auth_db.update_user(current_user)
        
        flash('Your password has been changed successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)


@app.endpoint('auth.forgot_password')
def forgot_password():
    """Forgot password - send OTP to email"""
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = auth_db.get_user(form.email.data)
        
        if user:
            # Generate OTP for password reset
            user.generate_otp()
            auth_db.update_user(user)
            
            # Send OTP email
            send_otp_email(user.email, user.otp_code)
            
            # Store email in session for reset page
            session['reset_email'] = user.email
            
            flash(f'An OTP code has been sent to {user.email}. Please check your email.', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            # Don't reveal if email exists or not for security
            flash(f'If an account exists with {form.email.data}, an OTP code has been sent.', 'info')
    
    return render_template('auth/forgot_password.html', form=form)


@app.endpoint('auth.reset_password')
def reset_password():
    """Reset password with OTP verification"""
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    # Get email from session
    email = session.get('reset_email')
    if not email:
        flash('Please start the password reset process by entering your email.', 'warning')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    # Pre-fill email from session
    if request.method == 'GET':
        form.email.data = email
    
    if form.validate_on_submit():
        user = auth_db.get_user(form.email.data)
        
        if not user:
            flash('User not found.', 'danger')
            session.pop('reset_email', None)
            return redirect(url_for('auth.forgot_password'))
        
        # Verify OTP
        if user.verify_otp(form.otp.data):
            # OTP is valid, update password
            user.set_password(form.new_password.data)
            auth_db.update_user(user)
            
            # Clear session
            session.pop('reset_email', None)
            
            flash('Your password has been reset successfully! You can now log in with your new password.', 'success')
            return redirect(url_for('auth.login'))
        else:
            if not user.is_otp_valid():
                flash('OTP has expired. Please request a new one.', 'danger')
                session.pop('reset_email', None)
                return redirect(url_for('auth.forgot_password'))
            else:
                flash('Invalid OTP code. Please try again.', 'danger')
    
    return render_template('auth/reset_password.html', form=form, email=email)


@app.endpoint('auth.resend_reset_otp')
def resend_reset_otp():
    """Resend OTP code for password reset"""
    email = session.get('reset_email')
    if not email:
        flash('No pending password reset found.', 'warning')
        return redirect(url_for('auth.forgot_password'))
    
    user = auth_db.get_user(email)
    if not user:
        flash('User not found.', 'danger')
        session.pop('reset_email', None)
        return redirect(url_for('auth.forgot_password'))
    
    # Generate new OTP
    user.generate_otp()
    auth_db.update_user(user)
    
    # Send email
    send_otp_email(user.email, user.otp_code)
    
    flash('A new OTP code has been sent to your email.', 'success')
    return redirect(url_for('auth.reset_password'))
