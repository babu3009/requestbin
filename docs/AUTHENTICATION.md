# Authentication System for RequestBin

## Overview

RequestBin includes a comprehensive authentication and user management system with **two-tier security**:

1. **Email Verification (Tier 1)**: ALL users must verify their email via OTP before accessing the system
2. **Admin Approval (Tier 2)**: Users from non-auto-approve domains require admin approval

Only authenticated, email-verified, and approved users can create request bins.

## Features

- **User Registration**: Users can register with their email and password
- **Email Verification**: OTP-based email verification for ALL users (except admins)
- **Admin Approval Workflow**: Users from non-auto-approve domains require admin approval
- **Auto-Approval Domains**: Configure domains for automatic approval after email verification
- **Admin Dashboard**: Administrators can manage users and approvals
- **Email Verification Status**: Admin dashboard shows verification status for all users
- **Default Admin User**: Automatically created on first run (bypasses email verification)

## Configuration

### Environment Variables

```bash
# Admin credentials (CHANGE IN PRODUCTION!)
ADMIN_EMAIL=admin@requestbin.local
ADMIN_PASSWORD=admin123

# Auto-approve domains (comma-separated)
AUTO_APPROVE_DOMAINS=tarento.com,ivolve.ai

# Flask secret key for sessions
FLASK_SESSION_SECRET_KEY=your-secret-key-here

# SMTP Configuration (for OTP emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
SMTP_FROM_EMAIL=noreply@requestbin.com
```

### SAP BTP Configuration

Add these to your `manifest-postgresql.yml`:

```yaml
env:
  ADMIN_EMAIL: admin@yourcompany.com
  ADMIN_PASSWORD: secure-password-here
  AUTO_APPROVE_DOMAINS: tarento.com,ivolve.ai,yourcompany.com
  
  # SMTP for OTP emails
  SMTP_HOST: smtp.gmail.com
  SMTP_PORT: 587
  SMTP_USER: your-email@example.com
  SMTP_PASSWORD: your-app-password
  SMTP_USE_TLS: "true"
  SMTP_FROM_EMAIL: noreply@requestbin.cfapps.eu10-004.hana.ondemand.com
```

## User Workflow

### 1. Registration

Users can register at `/register`:
- Enter email and password
- System generates 6-digit OTP code
- OTP email sent to user's address
- User redirected to email verification page

### 2. Email Verification

**All users (except admins) must verify their email:**
- User receives OTP email (valid for 24 hours)
- User enters 6-digit OTP at `/verify_email`
- System validates OTP and marks email as verified
- If OTP expired, user can request new OTP via "Resend OTP" button

**Auto-Approve Domains** (@tarento.com, @ivolve.ai):
- After email verification → Account auto-approved → Can login immediately

**Non-Auto-Approve Domains** (all others):
- After email verification → Account pending admin approval → Must wait for admin

### 3. Approval Process

**For users with non-auto-approve domains:**
- User verifies email via OTP
- User sees "Your account is pending approval by an administrator" message
- Admin logs in and visits `/admin/users`
- Admin sees user in "Pending Approvals" section with "Email Status: Verified" badge
- Admin clicks "Approve" button (only enabled for verified emails)
- User can now log in and create bins

**For users with auto-approve domains:**
- User verifies email via OTP
- Account automatically approved
- Can immediately log in and create bins

### 4. Login Flow

User authentication follows this sequence:
1. User enters email and password at `/login`
2. System checks credentials
3. **Step 1**: Check email verification status
   - If NOT verified → Redirect to `/verify_email` with OTP resend option
4. **Step 2**: Check approval status (non-auto-approve domains only)
   - If NOT approved → Show "Your account is pending approval" message
5. **Step 3**: If email verified AND approved → Login successful

### 5. Creating Bins

- User must be logged in, email-verified, AND approved
- Click "Create a RequestBin" on home page
- Bins are associated with the user account

## Admin Features

### Default Admin User

On first run, a default admin user is created:
- **Email**: `admin@requestbin.local` (or value of `ADMIN_EMAIL`)
- **Password**: `admin123` (or value of `ADMIN_PASSWORD`)
- **Bypasses**: Email verification (no OTP required)

**⚠️ IMPORTANT: Change the admin password in production!**

### Admin Dashboard

Accessible at `/admin/users` (admin-only):

**Pending Approvals Section:**
- View users awaiting approval
- See "Email Status" column:
  - 🟢 **Verified**: User has verified their email via OTP
  - 🔴 **Pending Verification**: User has not verified email yet
- Approve button:
  - **Enabled**: When email is verified
  - **Disabled**: When email is not verified (tooltip: "User must verify email first")
- Delete pending users

**All Users Section:**
- View all registered users
- Separate columns for:
  - **Email Status**: Verified / Not Verified
  - **Approval Status**: Approved / Pending / Admin
- Filter and manage users
- Delete non-admin users

### Admin Workflow for User Approval

```
1. User registers with @example.com email
   ↓
2. User verifies email via OTP
   ↓
3. Admin sees user in "Pending Approvals"
   ├─ Email Status: Verified ✓
   └─ Approve button: Enabled
   ↓
4. Admin clicks "Approve"
   ↓
5. User can now log in
```

**Important**: Admins cannot approve users who haven't verified their email. This prevents approving fake or typo'd email addresses.

## Database Schema

The authentication system adds a `users` table:

```sql
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    
    -- Email Verification Fields
    email_verified BOOLEAN DEFAULT FALSE,
    otp_code VARCHAR(6),
    otp_created_at TIMESTAMP,
    
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email_verified ON users(email_verified);
```

The `bins` table is enhanced with user ownership:

```sql
ALTER TABLE bins ADD COLUMN owner_email VARCHAR(255) REFERENCES users(email);
```

## API Changes

### Protected Endpoints

The following endpoint now requires authentication:

- `POST /api/v1/bins` - Create bin (requires login + email verification + approval)

**Response when not authenticated:**
```json
{
  "error": "Unauthorized"
}
```

**Response when email not verified:**
User is redirected to `/verify_email` page with OTP resend option.

**Response when not approved:**
```json
{
  "error": "Your account is pending approval"
}
```

## Deployment

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL and run schema:
```bash
psql -d requestbin -f schema.sql
```

3. Configure environment:
```bash
export STORAGE_BACKEND=postgresql
export REALM=prod
export ADMIN_EMAIL=admin@example.com
export ADMIN_PASSWORD=changeme123
export AUTO_APPROVE_DOMAINS=tarento.com,ivolve.ai

# Optional: SMTP for OTP emails (if not set, OTP printed to console)
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@example.com
export SMTP_PASSWORD=your-app-password
export SMTP_USE_TLS=true
```

4. Run the application:
```bash
python web.py
```

5. Access admin panel:
- Navigate to `http://localhost:4000`
- Login with admin credentials
- Visit `/admin/users` to manage users

### SAP BTP Deployment

1. Update `manifest-postgresql.yml` with your admin credentials and SMTP settings

2. Deploy:
```bash
cf push -f manifest-postgresql.yml
```

3. The admin user is automatically created on first startup

## Security Considerations

1. **Change Default Credentials**: Update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in production
2. **Use Strong Passwords**: Passwords are hashed using Werkzeug's pbkdf2:sha256
3. **Secure Session Key**: Set a strong `FLASK_SESSION_SECRET_KEY`
4. **HTTPS Only**: Always use HTTPS in production (handled by SAP BTP)
5. **Domain Whitelisting**: Carefully configure `AUTO_APPROVE_DOMAINS`
6. **Email Verification**: ALL users (except admin) must verify email via OTP
7. **SMTP Security**: Use app passwords for Gmail, not regular passwords
8. **OTP Expiry**: OTP codes expire after 24 hours for security

## Email Verification Benefits

1. **Prevents Fake Registrations**: Users must prove email ownership
2. **Reduces Spam**: Admin only reviews verified users in approval queue
3. **Two-Layer Security**: Email verification + Admin approval for non-auto-approve domains
4. **Clean User Database**: No unverified/fake email addresses
5. **Audit Trail**: Clear separation between email verification and admin approval

## Auto-Approval Domains

Configure trusted domains for automatic user approval **after email verification**:

```bash
# Single domain
export AUTO_APPROVE_DOMAINS=mycompany.com

# Multiple domains (comma-separated)
export AUTO_APPROVE_DOMAINS=tarento.com,ivolve.ai,mycompany.com
```

**Use cases:**
- Corporate email domains
- Partner organizations
- Trusted contractors

## User Management

### Approving Users

1. Log in as admin
2. Navigate to `/admin/users`
3. Review pending users
4. Click "Approve" or "Reject"

### Deleting Users

1. Navigate to `/admin/users`
2. Find the user in "All Users" table
3. Click "Delete" (admin users cannot be deleted)

## Testing

Test the authentication system:

```bash
# Test registration (sends OTP email)
curl -X POST http://localhost:4000/register \
  -d "email=test@tarento.com&password=test123&password2=test123"

# Check console for OTP code (development mode)

# Test email verification
curl -X POST http://localhost:4000/verify_email \
  -d "otp=123456"

# Test login (after email verification)
curl -X POST http://localhost:4000/login \
  -d "email=test@tarento.com&password=test123"

# Test bin creation (requires auth cookie + email verified + approved)
curl -X POST http://localhost:4000/api/v1/bins \
  -b cookies.txt \
  -d "private=false"
```

## Troubleshooting

### "Admin user already exists" on startup

This is normal - the system checks and creates admin only if it doesn't exist.

### Users can't create bins

1. Check if user is logged in
2. **Verify email is verified**: Check `/admin/users` for email status
3. Verify user is approved: `/admin/users`
4. Check browser console for JavaScript errors

### OTP email not received

1. **Development Mode**: Check console output for OTP code
2. **Production Mode**: 
   - Verify SMTP configuration in environment variables
   - Check spam folder
   - Check application logs for email sending errors
   - For Gmail: Use app password, not regular password

### Cannot approve user

- **Check Email Status**: User must verify email via OTP first
- Approve button is disabled if email not verified
- Wait for user to complete email verification

### Auto-approval not working

1. Verify `AUTO_APPROVE_DOMAINS` is set correctly
2. Check domain matches exactly (case-insensitive)
3. Ensure domains are comma-separated without spaces
4. **Note**: Auto-approval only happens AFTER email verification

### Database errors on startup

1. Ensure schema.sql has been run
2. Verify PostgreSQL credentials
3. Check that `users` table exists with email verification columns

### OTP expired

- OTP codes expire after 24 hours
- User can click "Resend OTP" button to get new code
- Each new OTP invalidates the previous one

## Migration from Non-Auth Version

If you have an existing RequestBin deployment:

1. Run the updated schema.sql (it includes `IF NOT EXISTS` checks)
2. Existing bins will continue to work
3. Set admin credentials via environment variables
4. Deploy the updated code
5. Admin user will be created automatically

## Dependencies

New Python packages required:

```
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
```

These are already included in `requirements.txt`.
