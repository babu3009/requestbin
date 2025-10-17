-- RequestBin PostgreSQL Database Schema
-- This script creates the necessary tables for RequestBin storage

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS requestbin_app;

-- Set search path to use the schema
SET search_path TO requestbin_app;

-- Drop existing tables if they exist (for clean reinstall)
-- Uncomment the following lines if you want to reset the database
-- DROP TABLE IF EXISTS requestbin_app.requests CASCADE;
-- DROP TABLE IF NOT EXISTS requestbin_app.bins CASCADE;
-- DROP TABLE IF NOT EXISTS requestbin_app.stats CASCADE;
-- DROP TABLE IF NOT EXISTS requestbin_app.users CASCADE;

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    otp_code VARCHAR(6),
    otp_created_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create index on approval status for admin queries
CREATE INDEX IF NOT EXISTS idx_users_approved ON users(is_approved);
CREATE INDEX IF NOT EXISTS idx_users_admin ON users(is_admin);
CREATE INDEX IF NOT EXISTS idx_users_email_verified ON users(email_verified);

-- Create bins table to store bin metadata
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
    request_count INTEGER DEFAULT 0,
    owner_email VARCHAR(255) REFERENCES users(email) ON DELETE SET NULL
);

-- Create index on expires_at for efficient cleanup
CREATE INDEX IF NOT EXISTS idx_bins_expires_at ON bins(expires_at);

-- Create index on name for fast lookups
CREATE INDEX IF NOT EXISTS idx_bins_name ON bins(name);

-- Create index on owner_email for efficient user bin lookups
CREATE INDEX IF NOT EXISTS idx_bins_owner_email ON bins(owner_email);

-- Create requests table to store request data
CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    bin_name VARCHAR(255) NOT NULL REFERENCES bins(name) ON DELETE CASCADE,
    request_data BYTEA NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    request_order INTEGER NOT NULL
);

-- Create composite index for efficient bin request lookups
CREATE INDEX IF NOT EXISTS idx_requests_bin_name ON requests(bin_name, request_order DESC);

-- Create index on created_at for cleanup and analytics
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON requests(created_at);

-- Create stats table for global counters
CREATE TABLE IF NOT EXISTS stats (
    key VARCHAR(255) PRIMARY KEY,
    value BIGINT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Initialize stats with default values
INSERT INTO stats (key, value) 
VALUES ('total_requests', 0)
ON CONFLICT (key) DO NOTHING;

INSERT INTO stats (key, value) 
VALUES ('total_bins', 0)
ON CONFLICT (key) DO NOTHING;

-- Note: Admin user creation is handled by init_postgres_schema.py
-- which reads ADMIN_EMAIL and ADMIN_PASSWORD from environment variables

-- Create a function to automatically clean up expired bins
CREATE OR REPLACE FUNCTION cleanup_expired_bins()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM bins WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Create a view for bin statistics
CREATE OR REPLACE VIEW bin_stats AS
SELECT 
    b.name,
    b.created_at,
    b.expires_at,
    b.private,
    b.request_count,
    COUNT(r.id) as actual_request_count,
    EXTRACT(EPOCH FROM (b.expires_at - NOW())) / 3600 as hours_remaining
FROM bins b
LEFT JOIN requests r ON b.name = r.bin_name
WHERE b.expires_at > NOW()
GROUP BY b.name, b.created_at, b.expires_at, b.private, b.request_count;

-- Grant permissions (adjust as needed for your database user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA requestbin_app TO requestbin_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA requestbin_app TO requestbin_user;
-- GRANT USAGE ON SCHEMA requestbin_app TO requestbin_user;

-- Print success message
DO $$
BEGIN
    RAISE NOTICE 'RequestBin PostgreSQL schema created successfully in requestbin_app schema!';
    RAISE NOTICE 'Tables created: bins, requests, stats';
    RAISE NOTICE 'Indexes created for optimal performance';
    RAISE NOTICE 'View created: bin_stats';
END $$;
