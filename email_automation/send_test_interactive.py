import smtplib
import getpass
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Configuration
template_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/email_template.html'
image_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/image.png'
logo_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/logo.png'

# Proton Defaults
host = "127.0.0.1"
port = 1025
sender_email = "hello@8vitality.com"

# Interactive Inputs
print("-" * 30)
print("PROTON MAIL BRIDGE CONNECTION")
print("-" * 30)
username = "8vitality@proton.me"
print(f"Username: {username}")
password = getpass.getpass("Enter Proton Bridge Password (hidden): ").strip()

# Test Recipient
test_recipient = "test1@pmintro.com"
test_name = "Test User"

print(f"\nConnecting to Proton Mail Bridge at {host}:{port}...")

try:
    # Read HTML Template
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Personalize
    html_content = html_content.replace('[Client Name]', test_name)

    # Create Email
    msg = MIMEMultipart('related')
    msg['From'] = f"Infinite Vitality <{sender_email}>"
    msg['To'] = test_recipient
    msg['Subject'] = "The Year of the Fire Horse: A Gift for Your Health 🧧"

    # Encapsulate the plain and HTML versions of the message body
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    # Plain text fallback
    text_content = """
    Happy Chinese New Year!
    
    As we transition into 2026, we are welcoming the Year of the Fire Horse.
    I have returning from my break with a renewed focus on helping you cultivate a vibrant body.
    
    Special Offer: 90 Minutes for $80.
    Book here: https://william-leigh6091.clientsecure.me
    
    See my new website: https://8vitality.com
    """
    msgAlternative.attach(MIMEText(text_content, 'plain'))
    
    # HTML Version
    # We need to handle images by Content-ID for them to show inline without downloading
    html_content = html_content.replace('src="image.png"', 'src="cid:main_image"')
    html_content = html_content.replace('src="logo.png"', 'src="cid:logo_image"')
    
    msgAlternative.attach(MIMEText(html_content, 'html'))

    # Attach Images
    with open(image_path, 'rb') as f:
        img_data = f.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<main_image>')
        msg.attach(img)
        
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', '<logo_image>')
        msg.attach(logo)

    # Send
    print("Initiating SMTP_SSL connection...")
    with smtplib.SMTP_SSL(host, port, timeout=15) as server:
        # server.set_debuglevel(1) # Reduced noise for interactive mode
        
        print("Logging in...")
        server.login(username, password)
        
        print("Sending mail...")
        server.sendmail(sender_email, test_recipient, msg.as_string())
        
    print(f"\n✅ TEST EMAIL SENT SUCCESSFULLY to {test_recipient}")

except Exception as e:
    print(f"\n❌ FAILED to send email: {e}")
    if "[SSL: WRONG_VERSION_NUMBER]" in str(e):
        print("Tip: If SSL failed, the server might actually want STARTTLS.")
