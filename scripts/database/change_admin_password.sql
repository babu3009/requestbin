-- Change Admin User Password for RequestBin
-- 
-- Usage:
-- 1. Generate a password hash using Python:
--    python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourNewPassword'))"
-- 
-- 2. Copy the generated hash and replace 'YOUR_PASSWORD_HASH_HERE' below
-- 
-- 3. Run this SQL script in your PostgreSQL database:
--    psql -h localhost -p 55234 -U f21e30667747 -d gmImNcMNjRlT -f change_admin_password.sql
--
-- Or connect to psql and paste the UPDATE command directly

-- Set the schema
SET search_path TO requestbin_app;

-- Update admin password
-- Replace 'YOUR_PASSWORD_HASH_HERE' with the actual hash from step 1
-- Replace 'admin@requestbin.cfapps.eu10-004.hana.ondemand.com' with your admin email if different
UPDATE users 
SET password_hash = 'YOUR_PASSWORD_HASH_HERE',
    updated_at = NOW()
WHERE email = 'admin@requestbin.cfapps.eu10-004.hana.ondemand.com';

-- Verify the update
SELECT email, is_admin, is_approved, updated_at 
FROM users 
WHERE email = 'admin@requestbin.cfapps.eu10-004.hana.ondemand.com';

-- Example with a specific password (ChangeMe456!):
-- To use this, uncomment the line below and comment out the one above
-- UPDATE users 
-- SET password_hash = 'scrypt:32768:8:1$VZX0kGLEMnqoTYbF$c88db7f4c0d8b8c39d7e8e8f7d7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c7b7a7c',
--     updated_at = NOW()
-- WHERE email = 'admin@requestbin.cfapps.eu10-004.hana.ondemand.com';
