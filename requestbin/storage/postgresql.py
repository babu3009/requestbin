from __future__ import absolute_import

import time
import pickle
import traceback
import json
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from requestbin.models import Bin

from requestbin import config

class PostgreSQLStorage():
    """PostgreSQL storage backend for RequestBin"""
    
    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.connection_pool = None
        self._initialize_connection_pool()
        self._create_tables()

    def _initialize_connection_pool(self):
        """Initialize PostgreSQL connection pool"""
        try:
            # Try to get connection parameters from config
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                database=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                sslmode=config.POSTGRES_SSLMODE,
                connect_timeout=30,
                options=f'-c search_path={config.POSTGRES_SCHEMA}'
            )
        except Exception as e:
            print(f"Error initializing PostgreSQL connection pool: {e}")
            traceback.print_exc()
            raise

    def _get_connection(self):
        """Get a connection from the pool"""
        return self.connection_pool.getconn()

    def _put_connection(self, conn):
        """Return a connection to the pool"""
        self.connection_pool.putconn(conn)

    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create bins table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bins (
                    name VARCHAR(255) PRIMARY KEY,
                    created_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    private BOOLEAN DEFAULT FALSE,
                    color_r INTEGER,
                    color_g INTEGER,
                    color_b INTEGER,
                    secret_key BYTEA,
                    favicon_uri TEXT,
                    request_count INTEGER DEFAULT 0
                )
            """)
            
            # Create index on expires_at for cleanup
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_bins_expires_at 
                ON bins(expires_at)
            """)
            
            # Create requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id SERIAL PRIMARY KEY,
                    bin_name VARCHAR(255) NOT NULL REFERENCES bins(name) ON DELETE CASCADE,
                    request_data BYTEA NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    request_order INTEGER NOT NULL
                )
            """)
            
            # Create indexes for requests
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_requests_bin_name 
                ON requests(bin_name, request_order DESC)
            """)
            
            # Create stats table for global counters
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    key VARCHAR(255) PRIMARY KEY,
                    value BIGINT DEFAULT 0
                )
            """)
            
            # Initialize stats
            cursor.execute("""
                INSERT INTO stats (key, value) 
                VALUES ('total_requests', 0)
                ON CONFLICT (key) DO NOTHING
            """)
            
            conn.commit()
            cursor.close()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating tables: {e}")
            traceback.print_exc()
            raise
        finally:
            if conn:
                self._put_connection(conn)

    def _cleanup_expired_bins(self):
        """Remove expired bins from database"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bins WHERE expires_at < NOW()")
            conn.commit()
            cursor.close()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error cleaning up expired bins: {e}")
        finally:
            if conn:
                self._put_connection(conn)

    def create_bin(self, private=False, custom_name=None, owner_email=None) -> Bin:
        """Create a new bin"""
        bin = Bin(private, custom_name, owner_email)
        conn = None
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            expires_at = time.time() + self.bin_ttl
            
            cursor.execute("""
                INSERT INTO bins (
                    name, created_at, expires_at, private, 
                    color_r, color_g, color_b, secret_key, favicon_uri, owner_email
                ) VALUES (
                    %s, to_timestamp(%s), to_timestamp(%s), %s, 
                    %s, %s, %s, %s, %s, %s
                )
            """, (
                bin.name,
                bin.created,
                expires_at,
                bin.private,
                bin.color[0],
                bin.color[1],
                bin.color[2],
                bin.secret_key,
                bin.favicon_uri,
                owner_email
            ))
            
            conn.commit()
            cursor.close()
            
            return bin
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating bin: {e}")
            traceback.print_exc()
            raise
        finally:
            if conn:
                self._put_connection(conn)

    def create_request(self, bin: Bin, request):
        """Add a request to a bin"""
        conn = None
        
        try:
            # bin.add() creates a Request object and inserts it at position 0
            bin.add(request)
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get current request count for this bin
            cursor.execute(
                "SELECT request_count FROM bins WHERE name = %s",
                (bin.name,)
            )
            result = cursor.fetchone()
            current_count = result[0] if result else 0
            
            # Serialize the Request model object (not the Flask request)
            # The Request object is at bin.requests[0] after bin.add()
            request_obj = bin.requests[0]
            request_data = pickle.dumps(request_obj)
            request_order = len(bin.requests) - 1
            
            # Insert the new request
            cursor.execute("""
                INSERT INTO requests (bin_name, request_data, request_order)
                VALUES (%s, %s, %s)
            """, (bin.name, request_data, request_order))
            
            # Update bin request count
            cursor.execute("""
                UPDATE bins SET request_count = request_count + 1
                WHERE name = %s
            """, (bin.name,))
            
            # Keep only the last MAX_REQUESTS
            cursor.execute("""
                DELETE FROM requests 
                WHERE bin_name = %s 
                AND request_order < (
                    SELECT request_order 
                    FROM requests 
                    WHERE bin_name = %s 
                    ORDER BY request_order DESC 
                    LIMIT 1 OFFSET %s
                )
            """, (bin.name, bin.name, config.MAX_REQUESTS - 1))
            
            # Update global request counter
            cursor.execute("""
                UPDATE stats SET value = value + 1 WHERE key = 'total_requests'
            """)
            
            conn.commit()
            cursor.close()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating request: {e}")
            traceback.print_exc()
            raise
        finally:
            if conn:
                self._put_connection(conn)

    def lookup_bin(self, name):
        """Retrieve a bin by name with all its requests"""
        conn = None
        
        try:
            # Clean up expired bins first
            self._cleanup_expired_bins()
            
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get bin metadata
            cursor.execute("""
                SELECT name, created_at, private, color_r, color_g, color_b,
                       secret_key, favicon_uri, request_count, owner_email
                FROM bins
                WHERE name = %s AND expires_at > NOW()
            """, (name,))
            
            bin_data = cursor.fetchone()
            
            if not bin_data:
                cursor.close()
                raise KeyError("Bin not found")
            
            # Reconstruct the Bin object
            bin = Bin()
            bin.name = bin_data['name']
            bin.created = bin_data['created_at'].timestamp()
            bin.private = bin_data['private']
            bin.color = (bin_data['color_r'], bin_data['color_g'], bin_data['color_b'])
            bin.secret_key = bytes(bin_data['secret_key']) if bin_data['secret_key'] else None
            bin.favicon_uri = bin_data['favicon_uri']
            bin.owner_email = bin_data.get('owner_email')
            # Note: request_count is a @property, calculated from len(bin.requests)
            
            # Get all requests for this bin
            cursor.execute("""
                SELECT request_data
                FROM requests
                WHERE bin_name = %s
                ORDER BY request_order DESC
                LIMIT %s
            """, (name, config.MAX_REQUESTS))
            
            requests = cursor.fetchall()
            bin.requests = [pickle.loads(bytes(r['request_data'])) for r in requests]
            
            cursor.close()
            return bin
            
        except KeyError:
            raise
        except Exception as e:
            print(f"Error looking up bin: {e}")
            traceback.print_exc()
            raise KeyError("Bin not found")
        finally:
            if conn:
                self._put_connection(conn)

    def get_bins_by_owner(self, owner_email):
        """Retrieve all bins owned by a specific user"""
        conn = None
        bins = []
        
        try:
            # Clean up expired bins first
            self._cleanup_expired_bins()
            
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all bins for this owner that haven't expired
            cursor.execute("""
                SELECT name, created_at, private, color_r, color_g, color_b,
                       secret_key, favicon_uri, owner_email
                FROM bins
                WHERE owner_email = %s AND expires_at > NOW()
                ORDER BY created_at DESC
            """, (owner_email,))
            
            bin_rows = cursor.fetchall()
            
            for bin_data in bin_rows:
                # Reconstruct each Bin object
                bin = Bin()
                bin.name = bin_data['name']
                bin.created = bin_data['created_at'].timestamp()
                bin.private = bin_data['private']
                bin.color = (bin_data['color_r'], bin_data['color_g'], bin_data['color_b'])
                bin.secret_key = bytes(bin_data['secret_key']) if bin_data['secret_key'] else None
                bin.favicon_uri = bin_data['favicon_uri']
                bin.owner_email = bin_data['owner_email']
                
                # Get requests for this bin (limit to recent ones for performance)
                cursor.execute("""
                    SELECT request_data
                    FROM requests
                    WHERE bin_name = %s
                    ORDER BY request_order DESC
                    LIMIT %s
                """, (bin.name, config.MAX_REQUESTS))
                
                requests = cursor.fetchall()
                bin.requests = [pickle.loads(bytes(r['request_data'])) for r in requests]
                
                bins.append(bin)
            
            cursor.close()
            return bins
            
        except Exception as e:
            print(f"Error getting bins by owner: {e}")
            traceback.print_exc()
            return []
        finally:
            if conn:
                self._put_connection(conn)

    def count_bins(self):
        """Count total number of active bins"""
        conn = None
        try:
            self._cleanup_expired_bins()
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM bins WHERE expires_at > NOW()")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print(f"Error counting bins: {e}")
            return 0
        finally:
            if conn:
                self._put_connection(conn)

    def count_requests(self):
        """Count total number of requests"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM stats WHERE key = 'total_requests'")
            result = cursor.fetchone()
            cursor.close()
            return int(result[0]) if result else 0
        except Exception as e:
            print(f"Error counting requests: {e}")
            return 0
        finally:
            if conn:
                self._put_connection(conn)

    def avg_req_size(self):
        """Calculate average request size in KB"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(LENGTH(request_data)) / 1024.0 as avg_size
                FROM requests
            """)
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result and result[0] else 0
        except Exception as e:
            print(f"Error calculating average request size: {e}")
            return 0
        finally:
            if conn:
                self._put_connection(conn)

    def __del__(self):
        """Cleanup connection pool on deletion"""
        if self.connection_pool:
            self.connection_pool.closeall()
