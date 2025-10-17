# Password Management Features

This document describes the password management features available in RequestBin, including changing passwords for logged-in users and resetting forgotten passwords using OTP verification.

## Features

### 1. Change Password (Logged-in Users)

**Purpose:** Allows authenticated users to update their password while logged in.

**Access:** Available from the user profile page

**URL:** `/auth/change-password`

**Process:**
1. User navigates to their profile and clicks "Change Password"
2. Form requires:
   - Current password (for verification)
   - New password (minimum 8 characters)
   - Confirm new password (must match)
3. System validates current password
4. If valid, updates to new password
5. User remains logged in with new credentials

**Security Features:**
- Requires authentication (`@login_required`)
- Validates current password before allowing change
- Enforces minimum password length (8 characters)
- Password confirmation to prevent typos
- Passwords are hashed using Werkzeug security

### 2. Forgot Password (Password Reset with OTP)

**Purpose:** Allows users who have forgotten their password to reset it securely using OTP email verification.

**Access:** Available from the login page

**URLs:**
- `/auth/forgot-password` - Request OTP
- `/auth/reset-password` - Reset password with OTP

**Process:**

#### Step 1: Request OTP
1. User clicks "Forgot your password?" on login page
2. Enters their email address
3. System:
   - Generates 6-digit OTP code
   - Stores OTP with timestamp in database
   - Sends OTP via email
   - Stores email in session for next step
4. User receives email with OTP code

#### Step 2: Reset Password
1. User is redirected to reset password page
2. Form displays (pre-filled email from session):
   - Email (readonly)
   - OTP code (6 digits)
   - New password (minimum 8 characters)
   - Confirm new password
3. User enters OTP from email and new password
4. System validates:
   - OTP matches stored code
   - OTP is not expired (24-hour validity)
   - Passwords match
5. If valid:
   - Updates password
   - Clears OTP from database
   - Clears session
   - Redirects to login with success message

**Security Features:**
- OTP is single-use (cleared after successful reset)
- OTP expires after 24 hours
- Email is stored in session (not exposed in URL)
- Does not reveal whether email exists in system
- Passwords are hashed using Werkzeug security
- OTP sent via secure SMTP connection

### 3. Resend OTP

**Purpose:** Allows users to request a new OTP if the original has expired or was not received.

**URLs:**
- `/auth/resend-reset-otp` - For password reset flow

**Process:**
1. User clicks "Resend OTP" link
2. System generates new OTP
3. Sends new OTP via email
4. Old OTP is replaced with new one

## Implementation Details

### Forms (requestbin/forms.py)

```python
class ChangePasswordForm(FlaskForm):
    """Change password form for logged-in users"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    new_password2 = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')


class ForgotPasswordForm(FlaskForm):
    """Forgot password form to request OTP"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send OTP')


class ResetPasswordForm(FlaskForm):
    """Reset password form with OTP verification"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    otp = StringField('OTP Code', validators=[
        DataRequired(), 
        Length(min=6, max=6, message='OTP must be 6 digits')
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    new_password2 = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')
```

### Views (requestbin/auth_views.py)

#### Change Password View
```python
@app.endpoint('auth.change_password')
@login_required
def change_password():
    """Change password for logged-in user"""
    # Validates current password
    # Updates to new password
    # Keeps user logged in
```

#### Forgot Password View
```python
@app.endpoint('auth.forgot_password')
def forgot_password():
    """Forgot password - send OTP to email"""
    # Generates OTP
    # Sends email
    # Stores email in session
    # Redirects to reset page
```

#### Reset Password View
```python
@app.endpoint('auth.reset_password')
def reset_password():
    """Reset password with OTP verification"""
    # Retrieves email from session
    # Validates OTP
    # Updates password
    # Clears session
    # Redirects to login
```

### Templates

1. **change_password.html** - Form for logged-in users to change password
2. **forgot_password.html** - Email input to request OTP
3. **reset_password.html** - OTP verification and new password entry

### User Model Methods (requestbin/auth.py)

The password reset functionality leverages existing OTP methods:

```python
def generate_otp(self):
    """Generate a new OTP code"""
    # Creates 6-digit code
    # Sets expiration timestamp
    
def verify_otp(self, otp_code):
    """Verify OTP code"""
    # Checks code matches
    # Checks not expired
    # Marks email as verified
    # Clears OTP after use
    
def is_otp_valid(self):
    """Check if OTP is still valid"""
    # Returns True if not expired
    
def set_password(self, password):
    """Set hashed password"""
    # Uses Werkzeug generate_password_hash
    
def check_password(self, password):
    """Verify password"""
    # Uses Werkzeug check_password_hash
```

## User Experience

### Change Password Flow
1. Login → Profile page
2. Click "Change Password" button
3. Enter current password
4. Enter new password (twice)
5. Submit form
6. See success message
7. Continue using app with new password

### Forgot Password Flow
1. Go to login page
2. Click "Forgot your password?" link
3. Enter email address
4. Submit form
5. Check email for OTP code
6. Enter OTP and new password (twice)
7. Submit form
8. See success message
9. Login with new password

## Email Template

The OTP email sent for password reset uses the same template as registration verification:

**Subject:** RequestBin - Password Reset OTP

**Body:**
```
Your OTP code for RequestBin password reset is: [6-DIGIT-CODE]

This code will expire in 24 hours.

If you did not request a password reset, please ignore this email.
```

## Configuration

Password management uses existing configuration:

```python
# SMTP Configuration (for OTP emails)
SMTP_HOST = 'smtp-relay.brevo.com'
SMTP_PORT = 587
SMTP_USER = 'your-smtp-user'
SMTP_PASSWORD = 'your-smtp-password'
SMTP_FROM_EMAIL = 'noreply@requestbin.com'

# Session Configuration (for storing reset email)
SESSION_SECRET_KEY = 'your-secret-key'
```

## Security Considerations

1. **OTP Security:**
   - 6-digit codes provide sufficient entropy (1 million combinations)
   - 24-hour expiration prevents brute force attacks
   - Single-use codes (cleared after successful reset)
   - Rate limiting could be added for additional security

2. **Password Security:**
   - Minimum 8 characters enforced
   - Passwords hashed using Werkzeug (PBKDF2 with salt)
   - Current password required for authenticated changes
   - Confirmation field prevents typos

3. **Email Security:**
   - SMTP over TLS (port 587)
   - Email stored in session (not URL parameters)
   - System doesn't reveal if email exists (forgot password)

4. **Session Security:**
   - Session secret key required
   - Session data cleared after successful reset
   - Session cookies are httponly

## Testing

### Test Change Password
1. Login as test user
2. Navigate to profile
3. Click "Change Password"
4. Test validation:
   - Wrong current password → Error message
   - Mismatched new passwords → Error message
   - Short password (< 8 chars) → Error message
   - Valid change → Success message
5. Logout and login with new password

### Test Forgot Password
1. From login page, click "Forgot your password?"
2. Enter valid email
3. Check email for OTP
4. Test OTP validation:
   - Wrong OTP → Error message
   - Expired OTP → Error message
   - Mismatched passwords → Error message
   - Short password → Error message
   - Valid reset → Success and redirect to login
5. Login with new password

### Test Resend OTP
1. During password reset, click "Resend OTP"
2. Verify new email received
3. Old OTP should not work
4. New OTP should work

## Admin Password Reset

Administrators can also reset their own passwords using the forgot password flow. For database-level admin password changes, use the provided utilities:

- `change_password.py` - Direct database password update
- `generate_password_sql.py` - Generate SQL for password change

See `AUTH_IMPLEMENTATION.md` for details on admin password management.

## Future Enhancements

Potential improvements for password management:

1. **Password Strength Meter** - Visual indicator of password strength
2. **Password History** - Prevent reuse of recent passwords
3. **Account Lockout** - Lock account after failed attempts
4. **2FA Integration** - Two-factor authentication option
5. **Password Expiration** - Force periodic password changes
6. **Email Notifications** - Alert user when password is changed
7. **Rate Limiting** - Limit OTP requests per email/IP
8. **SMS OTP Option** - Alternative to email OTP

## Troubleshooting

### OTP Email Not Received
1. Check spam/junk folder
2. Verify SMTP configuration in environment variables
3. Check email service logs
4. Use "Resend OTP" link

### OTP Expired
1. Click "Resend OTP" to generate new code
2. Complete reset within 24 hours

### Change Password Not Working
1. Verify current password is correct
2. Ensure new password meets requirements (8+ characters)
3. Ensure new passwords match
4. Check if logged in (session not expired)

### Session Lost During Reset
1. Session data may be cleared if browser closed
2. Return to forgot password page to restart process
3. Session persists across page refreshes

## Related Documentation

- `AUTHENTICATION.md` - Overview of authentication system
- `AUTH_IMPLEMENTATION.md` - Technical implementation details
- `OTP_VERIFICATION.md` - OTP email verification system
- `CONFIG_UPDATE.md` - Environment configuration guide
