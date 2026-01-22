import csv
import re
import os

# Paths
base_dir = '/Users/dr.leigh/Desktop/8Vitality.com/CLIENT_DATA_SAFE'
input_file = os.path.join(base_dir, 'Email Client List .csv')
output_file = os.path.join(base_dir, 'clean_list.csv')

# Regex for email validation
email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

cleaned_clients = []
seen_emails = set()

# Keywords to filter out (Test accounts, Billing, etc)
blocklist = {'test', 'mbo', 'pmintro', 'classpass', 'testing', 'verify', 'srhc', 'sacredrainhealing'}

print(f"Reading from: {input_file}")

try:
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        # Read all lines
        lines = f.readlines()

    for line in lines:
        # 1. Basic cleanup
        line = line.strip().replace('\u00a0', ' ') # Remove non-breaking spaces
        
        # 2. Skip obvious junk
        if not line or '```' in line or 'Here is' in line:
            continue
        if '@' not in line:
            continue

        # 3. Extract Email (Assume it's the last part after the last comma)
        # Note: Some lines are "Name,email". Some are "Name",email.
        last_comma = line.rfind(',')
        if last_comma == -1:
            continue
            
        raw_name = line[:last_comma].strip()
        email = line[last_comma+1:].strip()
        
        # Cleanup email
        email = email.lower().replace(',', '')
        
        if not email_pattern.match(email):
            continue
            
        # 4. Filter Garbage Accounts
        # Check if email is blocked domain
        if 'pmintro' in email or 'mindbodyonline' in email or 'classpass' in email:
            continue
            
        # Check name for "Test"
        name_lower = raw_name.lower()
        # Split into words to safely check "test" words
        name_words = re.split(r'[\s",]+', name_lower)
        if any(bad in name_words for bad in blocklist):
            continue

        # 5. Parse Name
        first_name = ""
        last_name = ""
        
        # Format 1: "LAST, FIRST" (has quotes or comma in name section)
        if '"' in raw_name or ',' in raw_name:
            # Remove quotes
            clean_raw = raw_name.replace('"', '')
            # If comma exists, split
            if ',' in clean_raw:
                parts = clean_raw.split(',')
                # Usually [Last, First]
                if len(parts) >= 2:
                    last_name = parts[0].strip().title()
                    first_name = parts[1].strip().title()
            else:
                # Just one name in quotes? Treat as first.
                first_name = clean_raw.strip().title()
        
        # Format 2: First Last (no quotes, space separated)
        else:
            parts = raw_name.split()
            if len(parts) > 0:
                first_name = parts[0].strip().title()
                if len(parts) > 1:
                    last_name = " ".join(parts[1:]).strip().title()
        
        # Fallback if parsing failed
        if not first_name:
            first_name = "Client"
        
        # Filter generic "Billing" names if desired, or keep them.
        # Keeping them for now, but user can review.

        # 6. Deduplicate
        if email in seen_emails:
            continue
        
        seen_emails.add(email)
        
        cleaned_clients.append({
            'First Name': first_name, 
            'Last Name': last_name, 
            'Email': email
        })

    # Sort alphabetically
    cleaned_clients.sort(key=lambda x: x['First Name'])

    # Write Result
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['First Name', 'Last Name', 'Email'])
        writer.writeheader()
        writer.writerows(cleaned_clients)

    print("-" * 30)
    print(f"REPORT:")
    print(f"Original Lines Read: {len(lines)}")
    print(f"Unique, Valid Clients: {len(cleaned_clients)}")
    print(f"Test/Junk Accounts Removed: {len(lines) - len(cleaned_clients)}")
    print(f"Saved to: {output_file}")
    print("-" * 30)
    print("Sample Entries:")
    for c in cleaned_clients[:5]:
        print(f" - {c['First Name']} {c['Last Name']} <{c['Email']}>")

except Exception as e:
    print(f"Error: {e}")
