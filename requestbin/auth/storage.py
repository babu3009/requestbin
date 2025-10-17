"""
PostgreSQL implementation of authentication storage
"""

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from requestbin.auth.models import AuthStorage, User
from requestbin import config
import time


class PostgreSQLAuthStorage(AuthStorage):
    """PostgreSQL backend for user authentication"""
    
    def __init__(self):
        """Initialize PostgreSQL connection pool"""
        self.pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            sslmode=config.POSTGRES_SSLMODE,
            options=f'-c search_path={config.POSTGRES_SCHEMA}'
        )
    
    def _get_connection(self):
        """Get a connection from the pool"""
        return self.pool.getconn()
    
    def _release_connection(self, conn):
        """Release connection back to the pool"""
        self.pool.putconn(conn)
    
    def create_user(self, email, password, is_admin=False):
        """Create a new user"""
        user = User(email=email, is_admin=is_admin)
        user.set_password(password)
        
        # Admin users: auto-approved and email verified (no OTP needed)
        # Regular users: all require email verification via OTP
        if is_admin:
            user.is_approved = True
            user.email_verified = True
            user.otp_code = None
            user.otp_created_at = None
        else:
            # All regular users get OTP for email verification
            user.email_verified = False
            user.generate_otp()
            
            # Auto-approve domains: approved but need email verification
            # Other domains: not approved AND need email verification
            user.is_approved = user.should_auto_approve()
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, is_admin, is_approved, email_verified, 
                                     otp_code, otp_created_at, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s))
                    """,
                    (user.email, user.password_hash, user.is_admin, user.is_approved, 
                     user.email_verified, user.otp_code, user.otp_created_at, user.created_at)
                )
                conn.commit()
            return user
        except psycopg2.IntegrityError:
            conn.rollback()
            raise ValueError(f"User {email} already exists")
        finally:
            self._release_connection(conn)
    
    def get_user(self, email):
        """Get user by email"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s",
                    (email,)
                )
                row = cursor.fetchone()
                if row:
                    return User(
                        email=row['email'],
                        password_hash=row['password_hash'],
                        is_admin=row['is_admin'],
                        is_approved=row['is_approved'],
                        email_verified=row.get('email_verified', False),
                        otp_code=row.get('otp_code'),
                        otp_created_at=row['otp_created_at'].timestamp() if row.get('otp_created_at') else None,
                        created_at=row['created_at'].timestamp(),
                        user_id=row['email']
                    )
                return None
        finally:
            self._release_connection(conn)
    
    def update_user(self, user):
        """Update user information"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                otp_created_ts = user.otp_created_at if user.otp_created_at else None
                cursor.execute(
                    """
                    UPDATE users 
                    SET password_hash = %s, is_admin = %s, is_approved = %s, 
                        email_verified = %s, otp_code = %s, 
                        otp_created_at = to_timestamp(%s), updated_at = NOW()
                    WHERE email = %s
                    """,
                    (user.password_hash, user.is_admin, user.is_approved, 
                     user.email_verified, user.otp_code, otp_created_ts, user.email)
                )
                conn.commit()
        finally:
            self._release_connection(conn)
    
    def delete_user(self, email):
        """Delete a user"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", (email,))
                conn.commit()
        finally:
            self._release_connection(conn)
    
    def get_all_users(self):
        """Get all users"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [
                    User(
                        email=row['email'],
                        password_hash=row['password_hash'],
                        is_admin=row['is_admin'],
                        is_approved=row['is_approved'],
                        email_verified=row.get('email_verified', False),
                        otp_code=row.get('otp_code'),
                        otp_created_at=row['otp_created_at'].timestamp() if row.get('otp_created_at') else None,
                        created_at=row['created_at'].timestamp(),
                        user_id=row['email']
                    )
                    for row in rows
                ]
        finally:
            self._release_connection(conn)
    
    def get_pending_users(self):
        """Get users pending approval"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE is_approved = FALSE ORDER BY created_at DESC"
                )
                rows = cursor.fetchall()
                return [
                    User(
                        email=row['email'],
                        password_hash=row['password_hash'],
                        is_admin=row['is_admin'],
                        is_approved=row['is_approved'],
                        email_verified=row.get('email_verified', False),
                        otp_code=row.get('otp_code'),
                        otp_created_at=row['otp_created_at'].timestamp() if row.get('otp_created_at') else None,
                        created_at=row['created_at'].timestamp(),
                        user_id=row['email']
                    )
                    for row in rows
                ]
        finally:
            self._release_connection(conn)
    
    def approve_user(self, email):
        """Approve a user"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET is_approved = TRUE, updated_at = NOW() WHERE email = %s",
                    (email,)
                )
                conn.commit()
        finally:
            self._release_connection(conn)
    
    def reject_user(self, email):
        """Reject/delete a user"""
        self.delete_user(email)
    
    def user_exists(self, email):
        """Check if user exists"""
        return self.get_user(email) is not None
    
    def initialize_admin(self):
        """Initialize default admin user if not exists"""
        if not self.user_exists(config.ADMIN_EMAIL):
            try:
                admin_user = self.create_user(
                    email=config.ADMIN_EMAIL,
                    password=config.ADMIN_PASSWORD,
                    is_admin=True
                )
                admin_user.is_approved = True
                admin_user.email_verified = True
                self.update_user(admin_user)
                return admin_user
            except ValueError:
                # Admin already exists
                pass
        return self.get_user(config.ADMIN_EMAIL)


# Memory-based authentication storage (for development/testing)
class MemoryAuthStorage(AuthStorage):
    """In-memory authentication storage for development"""
    
    def __init__(self):
        self.users = {}
        self.initialize_admin()
    
    def create_user(self, email, password, is_admin=False):
        """Create a new user"""
        if email in self.users:
            raise ValueError(f"User {email} already exists")
        
        user = User(email=email, is_admin=is_admin)
        user.set_password(password)
        
        # Admin users: auto-approved and email verified (no OTP needed)
        # Regular users: all require email verification via OTP
        if is_admin:
            user.is_approved = True
            user.email_verified = True
            user.otp_code = None
            user.otp_created_at = None
        else:
            # All regular users get OTP for email verification
            user.email_verified = False
            user.generate_otp()
            
            # Auto-approve domains: approved but need email verification
            # Other domains: not approved AND need email verification
            user.is_approved = user.should_auto_approve()
        
        self.users[email] = user
        return user
    
    def get_user(self, email):
        """Get user by email"""
        return self.users.get(email)
    
    def update_user(self, user):
        """Update user information"""
        self.users[user.email] = user
    
    def delete_user(self, email):
        """Delete a user"""
        if email in self.users:
            del self.users[email]
    
    def get_all_users(self):
        """Get all users"""
        return list(self.users.values())
    
    def get_pending_users(self):
        """Get users pending approval"""
        return [u for u in self.users.values() if not u.is_approved]
    
    def approve_user(self, email):
        """Approve a user"""
        if email in self.users:
            self.users[email].is_approved = True
    
    def reject_user(self, email):
        """Reject/delete a user"""
        self.delete_user(email)
    
    def user_exists(self, email):
        """Check if user exists"""
        return email in self.users
    
    def initialize_admin(self):
        """Initialize default admin user"""
        if config.ADMIN_EMAIL not in self.users:
            try:
                admin_user = self.create_user(
                    email=config.ADMIN_EMAIL,
                    password=config.ADMIN_PASSWORD,
                    is_admin=True
                )
                admin_user.is_approved = True
                admin_user.email_verified = True
                self.users[admin_user.email] = admin_user
            except ValueError:
                pass
        return self.users.get(config.ADMIN_EMAIL)
