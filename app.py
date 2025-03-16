import imaplib
import email
import re
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm

# IMAP settings for Gmail
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Function to connect to Gmail using IMAP
def connect_gmail(email_user, email_pass):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_user, email_pass)
        return mail
    except imaplib.IMAP4.error:
        st.error("Login failed! Please check your credentials.")
        return None

# Function to fetch top senders
def get_top_senders(mail, num_emails, num_senders=3):
    mail.select("INBOX")
    result, data = mail.search(None, "ALL")
    
    if result != "OK":
        st.error("Error retrieving emails.")
        return []

    email_ids = data[0].split()[-num_emails:]  # Get only the latest num_emails
    senders = []

    for email_id in tqdm(email_ids, desc=f"Fetching senders from last {num_emails} emails", unit="emails"):
        result, msg_data = mail.fetch(email_id, "(BODY.PEEK[HEADER])")
        if result != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg["From"]
                if sender:
                    match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
                    if match:
                        senders.append(match.group(0))

    top_senders = Counter(senders).most_common(num_senders)
    return top_senders

# Function to apply a "ToDelete" label
def mark_emails_for_deletion(mail, selected_senders):
    mail.select("INBOX")

    for sender in selected_senders:
        st.write(f"Marking emails from {sender}...")
        result, data = mail.search(None, f'FROM "{sender}"')
        if result != "OK":
            st.error(f"Error searching emails from {sender}")
            continue
        
        email_ids = data[0].split()
        for email_id in email_ids:
            mail.store(email_id, "+X-GM-LABELS", "ToDelete")

    st.success("\nEmails labeled 'ToDelete'. Review and delete them manually in Gmail.")

# Streamlit UI
st.title("📧 Inbox Zero: Bulk Email Cleaner For Gmail")

email_user = st.text_input("Enter your Gmail address:")
email_pass = st.text_input("Enter your App Password:", type="password") 

num_emails = st.number_input("How many recent emails do you want to analyze?", min_value=100, max_value=5000, step=100, value=500)

# Initialize session state for connection, senders, and selection states
if "mail" not in st.session_state:
    st.session_state.mail = None
if "top_senders" not in st.session_state:
    st.session_state.top_senders = {}
if "selected_senders" not in st.session_state:
    st.session_state.selected_senders = {}

if st.button("Fetch Top Senders"):
    if email_user and email_pass:
        # Display a progress bar
        progress_bar = st.progress(0)
        
        mail = connect_gmail(email_user, email_pass)
        if mail:
            # Update progress bar
            progress_bar.progress(25)
            
            top_senders = get_top_senders(mail, num_emails)
            if top_senders:
                # Update progress bar
                progress_bar.progress(75)
                
                st.session_state.mail = mail  # Store mail connection
                st.session_state.top_senders = {sender: count for sender, count in top_senders}
                # Initialize selection states
                st.session_state.selected_senders = {sender: False for sender in st.session_state.top_senders}

                st.success("Senders loaded! Select which ones to delete.")
            else:
                st.warning("No emails found!")
            # Complete the progress bar
            progress_bar.progress(100)
        else:
            st.warning("Failed to connect to Gmail. Check your credentials.")
            progress_bar.progress(0)
    else:
        st.warning("Please enter your email credentials.")

# Display table with checkboxes
if st.session_state.top_senders:
    st.write("### Top Senders in Your Gmail Inbox")
    for sender, count in st.session_state.top_senders.items():
        # Create a two-column layout
        col1, col2 = st.columns(2)
        
        # Use session state to maintain checkbox state
        with col1:
            st.session_state.selected_senders[sender] = st.checkbox(
                sender, 
                value=st.session_state.selected_senders[sender], 
                key=sender
            )
        
        with col2:
            st.write(f"{count} emails")

# Ensure senders are available before allowing selection
if st.session_state.top_senders:
    if st.button("Label Selected Emails for Deletion"):
        selected_senders = [sender for sender, selected in st.session_state.selected_senders.items() if selected]
        if selected_senders:
            if st.session_state.mail:
                mark_emails_for_deletion(st.session_state.mail, selected_senders)
                st.session_state.mail.logout()  # Logout after labeling emails
                st.session_state.mail = None  # Clear session state
            else:
                st.error("IMAP session expired. Please refresh and fetch senders again.")
        else:
            st.warning("No senders selected.")
