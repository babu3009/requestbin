"""
Email utility module for RequestBin
Handles OTP email sending via SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requestbin import config
import logging

logger = logging.getLogger(__name__)


def send_otp_email(user_email, otp_code, expiry_hours=24):
    """
    Send OTP verification email to user
    
    Args:
        user_email: User's email address
        otp_code: 6-digit OTP code
        expiry_hours: Hours until OTP expires (default: 24)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get SMTP configuration
        smtp_host = getattr(config, 'SMTP_HOST', None)
        smtp_port = getattr(config, 'SMTP_PORT', 587)
        smtp_user = getattr(config, 'SMTP_USER', None)
        smtp_password = getattr(config, 'SMTP_PASSWORD', None)
        smtp_use_tls = getattr(config, 'SMTP_USE_TLS', True)
        from_email = getattr(config, 'SMTP_FROM_EMAIL', smtp_user)
        
        # Check if SMTP is configured
        if not smtp_host or not smtp_user or not smtp_password:
            logger.warning(f"SMTP not configured. OTP for {user_email}: {otp_code}")
            # In development, just log the OTP
            print(f"\n{'='*60}")
            print(f"OTP EMAIL (Development Mode)")
            print(f"{'='*60}")
            print(f"To: {user_email}")
            print(f"Subject: Verify Your Email - RequestBin")
            print(f"\nYour OTP Code: {otp_code}")
            print(f"This code will expire in {expiry_hours} hours.")
            print(f"{'='*60}\n")
            return True
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Verify Your Email - RequestBin'
        msg['From'] = from_email
        msg['To'] = user_email
        
        # Create plain text version
        text_body = f"""
Hello,

Thank you for registering with RequestBin!

Your email verification code is: {otp_code}

This code will expire in {expiry_hours} hours.

If you didn't request this code, please ignore this email.

Best regards,
RequestBin Team
"""
        
        # Create HTML version
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #0088cc;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .otp-code {{
            background-color: #fff;
            border: 2px dashed #0088cc;
            padding: 20px;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 5px;
            color: #0088cc;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .expiry {{
            color: #999;
            font-size: 14px;
            text-align: center;
            margin-top: 10px;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Email Verification</h1>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>Thank you for registering with RequestBin! Please use the following code to verify your email address:</p>
            
            <div class="otp-code">{otp_code}</div>
            
            <div class="expiry">This code will expire in {expiry_hours} hours</div>
            
            <p style="margin-top: 30px;">If you didn't request this code, please ignore this email.</p>
            
            <p>Best regards,<br>RequestBin Team</p>
        </div>
        <div class="footer">
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach both versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email via SMTP
        if smtp_use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"OTP email sent successfully to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {user_email}: {str(e)}")
        # In development, still show OTP in console even if email fails
        print(f"\n{'='*60}")
        print(f"EMAIL FAILED - OTP for {user_email}: {otp_code}")
        print(f"Error: {str(e)}")
        print(f"{'='*60}\n")
        return False


def send_approval_notification(user_email):
    """
    Send email notification when account is approved
    
    Args:
        user_email: User's email address
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        smtp_host = getattr(config, 'SMTP_HOST', None)
        smtp_port = getattr(config, 'SMTP_PORT', 587)
        smtp_user = getattr(config, 'SMTP_USER', None)
        smtp_password = getattr(config, 'SMTP_PASSWORD', None)
        smtp_use_tls = getattr(config, 'SMTP_USE_TLS', True)
        from_email = getattr(config, 'SMTP_FROM_EMAIL', smtp_user)
        
        if not smtp_host or not smtp_user or not smtp_password:
            logger.warning(f"SMTP not configured. Approval notification for {user_email}")
            print(f"\n[INFO] Account approved for {user_email}\n")
            return True
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Your RequestBin Account Has Been Approved'
        msg['From'] = from_email
        msg['To'] = user_email
        
        text_body = f"""
Hello,

Good news! Your RequestBin account has been approved by an administrator.

You can now log in and start using RequestBin.

Best regards,
RequestBin Team
"""
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
        .content {{ background-color: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
        .button {{ display: inline-block; padding: 12px 30px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>Account Approved!</h1></div>
        <div class="content">
            <p>Hello,</p>
            <p>Good news! Your RequestBin account has been approved by an administrator.</p>
            <p>You can now log in and start using RequestBin.</p>
            <p>Best regards,<br>RequestBin Team</p>
        </div>
    </div>
</body>
</html>
"""
        
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        if smtp_use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Approval email sent successfully to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send approval email to {user_email}: {str(e)}")
        return False
