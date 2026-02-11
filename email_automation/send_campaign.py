import smtplib
import getpass
import time
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- Configuration ---
clean_list_path = '/Users/dr.leigh/Desktop/8Vitality.com/CLIENT_DATA_SAFE/clean_list.csv'
template_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/email_template.html'
image_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/image.png'
logo_path = '/Users/dr.leigh/Desktop/8Vitality.com/email_automation/logo.png'

host = "127.0.0.1"
port = 1025
sender_email = "hello@8vitality.com"
sender_name = "Infinite Vitality"

# --- Credentials ---
print("-" * 40)
print("🚀 MASS EMAIL LAUNCHPAD")
print("-" * 40)
print("Security Check: Please enter your Proton Mail Bridge Credentials.")
username = "8vitality@proton.me"
print(f"Username: {username}")
password = getpass.getpass("Password (hidden): ").strip()

# --- Load Data ---
html_template = ""
with open(template_path, 'r', encoding='utf-8') as f:
    html_template = f.read()

clients = []
with open(clean_list_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    clients = list(reader)

print(f"\nLoaded {len(clients)} clients from list.")
confirm = input("Type 'YES' to start sending to ALL clients: ")

if confirm != 'YES':
    print("Aborted.")
    exit()

# --- Send Loop ---
print("\nConnecting to Proton Mail Bridge...")
try:
    with smtplib.SMTP_SSL(host, port, timeout=20) as server:
        server.login(username, password)
        print("✅ Login Successful. Starting Send Sequence...\n")
        
        count = 0
        total = len(clients)
        
        for client in clients:
            first_name = client['First Name']
            email = client['Email']
            
            # Skip if missing email
            if not email or '@' not in email:
                continue

            print(f"[{count+1}/{total}] Sending to {first_name} <{email}>...", end='', flush=True)
            
            # --- Build Email ---
            msg = MIMEMultipart('related')
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = email
            msg['Subject'] = "The Year of the Fire Horse: A Gift for Your Health 🧧"

            msgAlternative = MIMEMultipart('alternative')
            msg.attach(msgAlternative)

            # Disclaimer for Unsubscribe (Plain Text)
            text_content = f"""
            Hi {first_name},
            
            Happy Chinese New Year!
            
            To view this email with images, please enable HTML or visit our website.
            
            Special Offer: 90 Minutes for $80.
            Book here: https://william-leigh6091.clientsecure.me
            
            Warmly,
            Dr. William Leigh
            Infinite Vitality
            """
            msgAlternative.attach(MIMEText(text_content, 'plain'))

            # Personalize HTML
            # Replace [Client Name] with actual First Name
            personal_html = html_template.replace('[Client Name]', first_name)
            
            # Embed Images (CID)
            personal_html = personal_html.replace('src="image.png"', 'src="cid:main_image"')
            personal_html = personal_html.replace('src="logo.png"', 'src="cid:logo_image"')
            
            msgAlternative.attach(MIMEText(personal_html, 'html'))

            # Attach Images
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<main_image>')
                msg.attach(img)
                
            with open(logo_path, 'rb') as f:
                logo = MIMEImage(f.read())
                logo.add_header('Content-ID', '<logo_image>')
                msg.attach(logo)
            
            # --- Send ---
            try:
                server.sendmail(sender_email, email, msg.as_string())
                print(" DONE.")
                count += 1
            except Exception as e:
                print(f" FAILED: {e}")
            
            # Rate Limit (Don't spam the bridge too fast)
            time.sleep(3) 

        print("-" * 40)
        print(f"🎉 MISSION COMPLETE. Sent {count}/{total} emails.")
        print("-" * 40)

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
