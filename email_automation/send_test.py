import smtplib
import configparser
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Configuration — paths relative to repo root, config path from env
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

config_path = os.environ.get("PROTON_CONFIG", os.path.join(REPO_ROOT, "CLIENT_DATA_SAFE", "proton_config.ini"))
template_path = os.path.join(SCRIPT_DIR, "email_template.html")
image_path = os.path.join(SCRIPT_DIR, "image.png")
logo_path = os.path.join(SCRIPT_DIR, "logo.png")

# Load Config
config = configparser.ConfigParser()
config.read(config_path)

try:
    host = config['proton_bridge']['host']
    port = int(config['proton_bridge']['port'])
    username = config['proton_bridge']['username']
    password = config['proton_bridge']['password']
    sender_email = config['proton_bridge']['sender_email']
except KeyError as e:
    print(f"Error reading config: Missing key {e}")
    exit(1)

# Test Recipient
test_recipient = "xepayac@gmail.com"
test_name = "Xepayac"

print(f"Connecting to Proton Mail Bridge at {host}:{port}...")

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
    # Replace <img src="image.png"> with <img src="cid:main_image">
    html_content = html_content.replace('src="image.png"', 'src="cid:main_image"')
    html_content = html_content.replace('src="logo.png"', 'src="cid:logo_image"')
    
    msgAlternative.attach(MIMEText(html_content, 'html'))

    # Attach Images
    # Main Image
    with open(image_path, 'rb') as f:
        img_data = f.read()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', '<main_image>')
        msg.attach(img)
        
    # Logo
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header('Content-ID', '<logo_image>')
        msg.attach(logo)

    # Send
    print("Initiating SMTP_SSL connection...")
    # Using SMTP_SSL because Bridge specifies 'SSL'
    with smtplib.SMTP_SSL(host, port, timeout=10) as server:
        server.set_debuglevel(1)
        print("Logging in...")
        server.login(username, password)
        print("Sending mail...")
        server.sendmail(sender_email, test_recipient, msg.as_string())
        
    print(f"✅ TEST EMAIL SENT SUCCESSFULLY to {test_recipient}")

except Exception as e:
    print(f"❌ FAILED to send email: {e}")
    if "[SSL: WRONG_VERSION_NUMBER]" in str(e):
        print("Tip: If SSL failed, the server might actually want STARTTLS. Let me know.")
