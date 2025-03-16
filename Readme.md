# 📧 Inbox Zero: Bulk Email Cleaner For Gmail

Gmail Bulk Email Cleaner is a Streamlit application that helps you identify and label emails from top senders in your Gmail inbox for deletion. This tool is useful for managing and cleaning up your inbox by marking emails from selected senders with a "ToDelete" label.

## Features

- Connect to your Gmail account using IMAP.
- Analyze a specified number of recent emails to identify top senders.
- Display top senders with the number of emails received.
- Select senders to label their emails for deletion.
- Mark selected emails with a "ToDelete" label for manual review and deletion in Gmail.

<img width="677" alt="tutorial" src="https://github.com/user-attachments/assets/14640f74-e0a4-4866-8a44-794116f4e346" />

## Prerequisites

- Python 3.7 or higher
- A Gmail account with IMAP access enabled
- An App Password for your Gmail account. Instructions to set that up: https://support.google.com/mail/answer/185833?hl=en

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/gmail-bulk-email-cleaner.git
   cd gmail-bulk-email-cleaner
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **Enter your Gmail credentials:**

   - Enter your Gmail address.
   - Enter your App Password (not your regular Gmail password).

3. **Analyze your inbox:**

   - Specify the number of recent emails to analyze (between 100 and 5000).
   - Click "Fetch Top Senders" to retrieve and display the top senders.

4. **Select senders to label for deletion:**

   - Use the checkboxes to select senders whose emails you want to label.
   - Click "Label Selected Emails for Deletion" to mark the emails.
   - Emails marked for deletion will be labeled in a folder called ToDelete . Navigate to this folder and manually delete all the emails.
   - Labeling emails with "ToDelete" is safer than deleting them in bulk, as it allows you to review the emails before permanently removing them.

5. **Review and delete emails:**

   - Log in to your Gmail account and review emails labeled "ToDelete".
   - Manually delete the emails if desired.


## License

This project is licensed under the MIT License.
