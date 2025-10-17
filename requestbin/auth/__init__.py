"""
Authentication package for RequestBin
Contains user authentication, forms, storage, and utilities
"""

from requestbin.auth.models import User
from requestbin.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from requestbin.auth.storage import PostgreSQLAuthStorage, MemoryAuthStorage
from requestbin.auth.utils import send_otp_email, send_approval_notification

__all__ = [
    'User',
    'LoginForm', 'RegistrationForm', 'ChangePasswordForm', 'ForgotPasswordForm', 'ResetPasswordForm',
    'PostgreSQLAuthStorage', 'MemoryAuthStorage',
    'send_otp_email', 'send_approval_notification'
]
