from requestbin import config
import os
from io import BytesIO

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO


class WSGIRawBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['raw'] = body
        environ['wsgi.input'] = BytesIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback



app = Flask(__name__)

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Import flask_socketio utilities for room management
from flask_socketio import emit, join_room, leave_room

# SocketIO event handlers
@socketio.on('join')
def on_join(data):
    """Handle client joining a bin-specific room"""
    bin_name = data.get('bin_name')
    if bin_name:
        join_room(bin_name)
        print(f"Client joined room: {bin_name}")

@socketio.on('leave')
def on_leave(data):
    """Handle client leaving a bin-specific room"""
    bin_name = data.get('bin_name')
    if bin_name:
        leave_room(bin_name)
        print(f"Client left room: {bin_name}")

@socketio.on('connect')
def on_connect():
    """Handle client connection"""
    print("Client connected")

@socketio.on('disconnect')
def on_disconnect():
    """Handle client disconnection"""
    print("Client disconnected")

if os.environ.get('ENABLE_CORS', config.ENABLE_CORS):
    cors = CORS(app, resources={r"*": {"origins": os.environ.get('CORS_ORIGINS', config.CORS_ORIGINS)}})

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = WSGIRawBody(ProxyFix(app.wsgi_app))

app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize authentication storage
if config.STORAGE_BACKEND == "requestbin.storage.postgresql.PostgreSQLStorage":
    from requestbin.auth.storage import PostgreSQLAuthStorage
    auth_db = PostgreSQLAuthStorage()
else:
    from requestbin.auth.storage import MemoryAuthStorage
    auth_db = MemoryAuthStorage()

# Initialize default admin user
auth_db.initialize_admin()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return auth_db.get_user(user_id)

if config.BUGSNAG_KEY:
    import bugsnag
    from bugsnag.flask import handle_exceptions
    bugsnag.configure(
        api_key=config.BUGSNAG_KEY,
        project_root=app.root_path,
        # 'production' is a magic string for bugsnag, rest are arbitrary
        release_stage = config.REALM.replace("prod", "production"),
        notify_release_stages=["production", "test"],
        use_ssl = True
    )
    handle_exceptions(app)

from requestbin.filters import *
app.jinja_env.filters['status_class'] = status_class
app.jinja_env.filters['friendly_time'] = friendly_time
app.jinja_env.filters['friendly_size'] = friendly_size
app.jinja_env.filters['to_qs'] = to_qs
app.jinja_env.filters['approximate_time'] = approximate_time
app.jinja_env.filters['exact_time'] = exact_time
app.jinja_env.filters['short_date'] = short_date
app.jinja_env.filters['format_datetime'] = format_datetime
app.jinja_env.filters['format_timezone'] = format_timezone

app.add_url_rule('/', 'views.home')
app.add_url_rule('/<path:name>', 'views.bin', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE'])

app.add_url_rule('/docs/<name>', 'views.docs')
app.add_url_rule('/about', 'views.about')

# Authentication routes
app.add_url_rule('/login', 'auth.login', methods=['GET', 'POST'])
app.add_url_rule('/logout', 'auth.logout')
app.add_url_rule('/register', 'auth.register', methods=['GET', 'POST'])
app.add_url_rule('/profile', 'auth.profile')
app.add_url_rule('/admin/users', 'auth.admin_users')
app.add_url_rule('/admin/approve/<email>', 'auth.approve_user', methods=['POST'])
app.add_url_rule('/admin/reject/<email>', 'auth.reject_user', methods=['POST'])
app.add_url_rule('/verify-email', 'auth.verify_email', methods=['GET', 'POST'])
app.add_url_rule('/resend-otp', 'auth.resend_otp', methods=['GET', 'POST'])

# Password management routes
app.add_url_rule('/auth/change-password', 'auth.change_password', methods=['GET', 'POST'])
app.add_url_rule('/auth/forgot-password', 'auth.forgot_password', methods=['GET', 'POST'])
app.add_url_rule('/auth/reset-password', 'auth.reset_password', methods=['GET', 'POST'])

# API routes
app.add_url_rule('/api/v1/bins', 'api.bins', methods=['POST'])
app.add_url_rule('/api/v1/bins/<name>', 'api.bin', methods=['GET'])
app.add_url_rule('/api/v1/bins/<bin>/requests', 'api.requests', methods=['GET'])
app.add_url_rule('/api/v1/bins/<bin>/requests/<name>', 'api.request', methods=['GET'])

app.add_url_rule('/api/v1/stats', 'api.stats')

# app.add_url_rule('/robots.txt', redirect_to=url_for('static', filename='robots.txt'))

# Import modules after app initialization
from requestbin.views import api, main, auth as auth_views
from requestbin.database import db

# Make db and socketio available at package level for backwards compatibility
__all__ = ['app', 'config', 'auth_db', 'db', 'socketio']
