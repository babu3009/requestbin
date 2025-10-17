"""
Authentication module for RequestBin
Handles user registration, login, approval workflow, and OTP email verification
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time
import secrets
import string
from requestbin import config


class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, email, password_hash=None, is_admin=False, is_approved=False, 
                 email_verified=False, otp_code=None, otp_created_at=None, 
                 created_at=None, user_id=None):
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.is_approved = is_approved
        self.email_verified = email_verified
        self.otp_code = otp_code
        self.otp_created_at = otp_created_at
        self.created_at = created_at or time.time()
        self.id = user_id or email  # Flask-Login requires 'id' attribute
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)
    
    def should_auto_approve(self):
        """Check if user's email domain should be auto-approved"""
        domain = self.email.split('@')[-1].lower()
        return domain in [d.strip().lower() for d in config.AUTO_APPROVE_DOMAINS]
    
    def generate_otp(self):
        """Generate a 6-digit OTP code"""
        self.otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        self.otp_created_at = time.time()
        return self.otp_code
    
    def verify_otp(self, otp):
        """Verify the provided OTP code"""
        if not self.otp_code or not self.otp_created_at:
            return False
        
        # Check if OTP has expired (24 hours = 86400 seconds)
        if not self.is_otp_valid():
            return False
        
        # Check if OTP matches
        if self.otp_code == otp:
            self.email_verified = True
            self.otp_code = None  # Clear OTP after successful verification
            self.otp_created_at = None
            return True
        
        return False
    
    def is_otp_valid(self):
        """Check if the current OTP is still valid (within 24 hours)"""
        if not self.otp_created_at:
            return False
        
        current_time = time.time()
        elapsed_time = current_time - self.otp_created_at
        
        # OTP valid for 24 hours (86400 seconds)
        return elapsed_time < 86400
    
    def get_otp_expiry_time(self):
        """Get remaining time until OTP expires (in seconds)"""
        if not self.otp_created_at:
            return 0
        
        current_time = time.time()
        elapsed_time = current_time - self.otp_created_at
        remaining_time = 86400 - elapsed_time  # 24 hours in seconds
        
        return max(0, remaining_time)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'email': self.email,
            'is_admin': self.is_admin,
            'is_approved': self.is_approved,
            'email_verified': self.email_verified,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class AuthStorage:
    """Base class for authentication storage"""
    
    def create_user(self, email, password, is_admin=False):
        """Create a new user"""
        raise NotImplementedError
    
    def get_user(self, email):
        """Get user by email"""
        raise NotImplementedError
    
    def update_user(self, user):
        """Update user information"""
        raise NotImplementedError
    
    def delete_user(self, email):
        """Delete a user"""
        raise NotImplementedError
    
    def get_all_users(self):
        """Get all users"""
        raise NotImplementedError
    
    def get_pending_users(self):
        """Get users pending approval"""
        raise NotImplementedError
    
    def approve_user(self, email):
        """Approve a user"""
        raise NotImplementedError
    
    def reject_user(self, email):
        """Reject/delete a user"""
        raise NotImplementedError
    
    def user_exists(self, email):
        """Check if user exists"""
        raise NotImplementedError
    
    def initialize_admin(self):
        """Initialize default admin user"""
        raise NotImplementedError
