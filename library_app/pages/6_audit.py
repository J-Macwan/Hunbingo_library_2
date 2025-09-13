import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

# Import from app.py
from app import (
    sidebar_nav
)

# Set page configuration
st.set_page_config(
    page_title="Audit Logs",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect if not logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login to access this page")
    st.switch_page("app.py")

# Check if admin
if st.session_state['role'] != 'admin':
    st.error("You don't have permission to access this page")
    st.switch_page("app.py")

# Show sidebar navigation
sidebar_nav()

# Paths for data files
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
LOGS_FILE = DATA_DIR / "audit_logs.pkl"

# Create audit logs file if it doesn't exist
if not LOGS_FILE.exists():
    audit_logs = []
    with open(LOGS_FILE, 'wb') as f:
        pickle.dump(audit_logs, f)

# Function to load audit logs
def load_audit_logs():
    with open(LOGS_FILE, 'rb') as f:
        return pickle.load(f)

# Function to save audit logs
def save_audit_logs(logs):
    with open(LOGS_FILE, 'wb') as f:
        pickle.dump(logs, f)

# Function to add audit log
def add_audit_log(action, details, username):
    logs = load_audit_logs()
    
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username': username,
        'action': action,
        'details': details
    }
    
    logs.append(log_entry)
    save_audit_logs(logs)

# Main content
st.title("Audit Logs")

# Add a sample log if not in session state
if 'sample_log_added' not in st.session_state:
    add_audit_log("Login", "Administrator logged in", "admin")
    add_audit_log("View Books", "Administrator viewed book list", "admin")
    st.session_state['sample_log_added'] = True

# Load audit logs
audit_logs = load_audit_logs()

# Filter options
st.sidebar.header("Filter Options")

# Date filter
start_date = st.sidebar.date_input("Start Date", datetime.now().replace(day=1))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Action filter
actions = ["All Actions"] + list(set(log['action'] for log in audit_logs))
selected_action = st.sidebar.selectbox("Action", actions)

# Username filter
usernames = ["All Users"] + list(set(log['username'] for log in audit_logs))
selected_username = st.sidebar.selectbox("Username", usernames)

# Apply filters
filtered_logs = []

for log in audit_logs:
    log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S').date()
    
    # Check date range
    if start_date <= log_time <= end_date:
        # Check action filter
        if selected_action == "All Actions" or log['action'] == selected_action:
            # Check username filter
            if selected_username == "All Users" or log['username'] == selected_username:
                filtered_logs.append(log)

# Display audit logs
if filtered_logs:
    # Sort logs by timestamp (most recent first)
    sorted_logs = sorted(filtered_logs, key=lambda x: x['timestamp'], reverse=True)
    
    # Convert to DataFrame for display
    logs_df = pd.DataFrame(sorted_logs)
    st.dataframe(logs_df, use_container_width=True)
    
    # Download as CSV
    csv = logs_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Logs as CSV",
        csv,
        "audit_logs.csv",
        "text/csv",
        key='download-csv'
    )
    
    # Log summary
    st.subheader("Log Summary")
    st.write(f"Total Logs: {len(filtered_logs)}")
    
    # Action counts
    action_counts = {}
    for log in filtered_logs:
        if log['action'] in action_counts:
            action_counts[log['action']] += 1
        else:
            action_counts[log['action']] = 1
    
    # Display action counts
    st.write("Actions:")
    for action, count in action_counts.items():
        st.write(f"- {action}: {count}")
else:
    st.info("No audit logs found for the selected filters")