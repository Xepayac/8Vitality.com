# Email Campaign Action Plan

## Phase 1: Data & Content Preparation
- [ ] **Prepare Client List Spreadsheet**
    - Ensure you have a `.csv` or `.xlsx` file with your clients.
    - **Clean the data**: Make sure there are no empty rows or duplicate emails.
    - **Verify Headers**: Ensure the first row has clear headers like `FirstName`, `Email`, `LastName`.
    - **Save File**: Save this file as `client_list.csv` (or `.xlsx`) in this `email_automation` folder.

- [ ] **Draft Your Message**
    - Write your email subject line.
    - Write your email body text.
    - **Mark Personalization**: Decide where you want the personal touches (e.g., "Hi {FirstName},").
    - Save this draft in a text file `email_draft.txt` or just keep it handy to paste into the script later.

## Phase 2: Technical Setup (Proton Mail)
- [ ] **Install Proton Mail Bridge**
    - Download and install the [Proton Mail Bridge](https://proton.me/mail/bridge) application on your Mac.
    - Open the app and log in with your Proton credentials.
- [ ] **Configure Bridge for IMAP/SMTP**
    - In the Bridge app, look for your account settings or "Mailbox details".
    - **IMPORTANT**: Note down the specific **Username** and **Password** provided by the Bridge (this is *different* from your normal login).
    - Note down the **SMTP Port** (usually `1025`) and **Host** (`127.0.0.1`).

## Phase 3: Automation Setup (Assistant & You)
- [ ] **Create Python Environment**
    - *Agent Action*: I will set up a Python script to handle the mailing.
    - *Agent Action*: I will install necessary libraries (like `pandas` for reading your spreadsheet).

- [ ] **Configure Script**
    - Input the Proton Bridge credentials (Username/Password/Port) into the secure script configuration.
    - Load the `client_list.csv`.
    - Load the email template.

## Phase 4: Testing & Sending
- [ ] **Test Run**
    - Add a "Test Client" to your list (use your own secondary email).
    - Run the script in "Test Mode" to send *only* to you.
    - Verify the email looks correct and personalization works.

- [ ] **Go Live**
    - Once confirmed, run the script for the full list.
    - Monitor the output log to ensure all emails are sent successfully.
