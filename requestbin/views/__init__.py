"""
Views package for RequestBin
Contains view controllers organized by functionality
"""

# Import views to make them available at package level
from requestbin.views import main, auth, api

__all__ = ['main', 'auth', 'api']
