"""
Kascade Cloud - Email Notifications
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.zoho.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'mizzle@dmds.site')
SMTP_PASS = os.getenv('SMTP_PASS', '')

def send_welcome_email(to_email, customer_name, plan):
    """Send welcome email to new customer"""
    subject = f"Welcome to Kascade Cloud - {plan.title()} Plan Activated!"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #00d4ff, #7c3aed); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .header h1 {{ color: white; margin: 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: linear-gradient(135deg, #00d4ff, #7c3aed); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; margin-top: 20px; }}
            .footer {{ text-align: center; padding: 20px; color: #888; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦅 Kascade Cloud</h1>
            </div>
            <div class="content">
                <h2>Welcome, {customer_name}!</h2>
                <p>Your <strong>{plan.title()}</strong> plan is now active.</p>
                <p>Your AI assistant is ready to:</p>
                <ul>
                    <li>Handle customer conversations on WhatsApp</li>
                    <li>Learn your business services and policies</li>
                    <li>Respond 24/7, never miss a lead</li>
                </ul>
                <a href="https://kascade-cloud.vercel.app/dashboard.html" class="button">Open Dashboard</a>
            </div>
            <div class="footer">
                <p>Questions? Reply to this email.</p>
                <p>© 2026 Kascade Security LLC</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'Kascade Cloud <{SMTP_USER}>'
    msg['To'] = to_email
    msg.attach(MIMEText(html, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"✅ Welcome email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_usage_alert(to_email, used, limit):
    """Send usage limit warning"""
    if limit == float('inf'):
        return
    
    percent = (used / limit) * 100
    if percent < 80:
        return
    
    subject = "Kascade Cloud - Usage Alert"
    html = f"""
    <h2>You're at {percent:.0f}% of your monthly messages</h2>
    <p>You've used {used:,} of {limit:,} messages.</p>
    <p>Upgrade your plan to get more messages.</p>
    <a href="https://kascade-cloud.vercel.app/signup.html">Upgrade Now</a>
    """
    
    print(f"⚠️ Usage alert sent to {to_email}")

if __name__ == '__main__':
    # Test email
    send_welcome_email('test@example.com', 'Test User', 'pro')
