import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

# Import from app.py
from app import (
    load_settings, save_settings,
    sidebar_nav
)

# Set page configuration
st.set_page_config(
    page_title="Settings & Preferences",
    page_icon="⚙️",
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

# Main content
st.title("Settings & Preferences")

# Load settings
settings = load_settings()

# Tabs for different settings
tab1, tab2, tab3 = st.tabs(["Library Info", "Fine Rules", "Backup/Restore"])

# Library Info Tab
with tab1:
    st.header("Library Information")
    
    library_name = st.text_input("Library Name", value=settings['library_name'])
    
    col1, col2 = st.columns(2)
    with col1:
        contact_email = st.text_input("Contact Email", value=settings['contact_email'])
    with col2:
        contact_phone = st.text_input("Contact Phone", value=settings['contact_phone'])
    
    operating_hours = st.text_input("Operating Hours", value=settings['operating_hours'])
    
    if st.button("Save Library Information"):
        # Update settings
        settings['library_name'] = library_name
        settings['contact_email'] = contact_email
        settings['contact_phone'] = contact_phone
        settings['operating_hours'] = operating_hours
        
        # Save settings
        save_settings(settings)
        
        st.success("Library information updated successfully")

# Fine Rules Tab
with tab2:
    st.header("Fine Rules Configuration")
    
    fine_per_day = st.number_input("Fine per Day (USD)", min_value=0.0, value=float(settings['fine_per_day']), step=0.25)
    max_books = st.number_input("Maximum Books per User", min_value=1, value=int(settings['max_books_per_user']))
    loan_period = st.number_input("Loan Period (Days)", min_value=1, value=int(settings['loan_period_days']))
    
    if st.button("Save Fine Rules"):
        # Update settings
        settings['fine_per_day'] = fine_per_day
        settings['max_books_per_user'] = max_books
        settings['loan_period_days'] = loan_period
        
        # Save settings
        save_settings(settings)
        
        st.success("Fine rules updated successfully")

# Backup/Restore Tab
with tab3:
    st.header("Backup/Restore Database")
    
    # Backup functionality
    st.subheader("Backup Database")
    
    if st.button("Create Backup"):
        # Get data
        DATA_DIR = Path(__file__).parent.parent / "data"
        USERS_FILE = DATA_DIR / "users.pkl"
        BOOKS_FILE = DATA_DIR / "books.pkl"
        ISSUES_FILE = DATA_DIR / "issues.pkl"
        SETTINGS_FILE = DATA_DIR / "settings.pkl"
        
        # Create backup directory if it doesn't exist
        BACKUP_DIR = DATA_DIR / "backups"
        BACKUP_DIR.mkdir(exist_ok=True)
        
        # Create backup timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Create backup files
        import shutil
        
        try:
            if USERS_FILE.exists():
                shutil.copy(USERS_FILE, BACKUP_DIR / f"users_{timestamp}.pkl")
            
            if BOOKS_FILE.exists():
                shutil.copy(BOOKS_FILE, BACKUP_DIR / f"books_{timestamp}.pkl")
            
            if ISSUES_FILE.exists():
                shutil.copy(ISSUES_FILE, BACKUP_DIR / f"issues_{timestamp}.pkl")
            
            if SETTINGS_FILE.exists():
                shutil.copy(SETTINGS_FILE, BACKUP_DIR / f"settings_{timestamp}.pkl")
            
            st.success(f"Backup created successfully: {timestamp}")
        except Exception as e:
            st.error(f"Backup failed: {str(e)}")
    
    # Restore functionality
    st.subheader("Restore Database")
    
    # Get backup files
    DATA_DIR = Path(__file__).parent.parent / "data"
    BACKUP_DIR = DATA_DIR / "backups"
    
    if BACKUP_DIR.exists():
        backup_timestamps = set()
        
        for file in BACKUP_DIR.glob("*_*.pkl"):
            parts = file.name.split("_")
            if len(parts) >= 3:
                date_part = parts[-3]
                time_part = parts[-2]
                timestamp = f"{date_part}_{time_part}"
                backup_timestamps.add(timestamp)
        
        if backup_timestamps:
            backup_list = sorted(list(backup_timestamps), reverse=True)
            selected_backup = st.selectbox("Select Backup to Restore", backup_list)
            
            if st.button("Restore Selected Backup"):
                # Get data files
                USERS_FILE = DATA_DIR / "users.pkl"
                BOOKS_FILE = DATA_DIR / "books.pkl"
                ISSUES_FILE = DATA_DIR / "issues.pkl"
                SETTINGS_FILE = DATA_DIR / "settings.pkl"
                
                # Get backup files
                USERS_BACKUP = BACKUP_DIR / f"users_{selected_backup}.pkl"
                BOOKS_BACKUP = BACKUP_DIR / f"books_{selected_backup}.pkl"
                ISSUES_BACKUP = BACKUP_DIR / f"issues_{selected_backup}.pkl"
                SETTINGS_BACKUP = BACKUP_DIR / f"settings_{selected_backup}.pkl"
                
                # Restore files
                import shutil
                
                try:
                    if USERS_BACKUP.exists():
                        shutil.copy(USERS_BACKUP, USERS_FILE)
                    
                    if BOOKS_BACKUP.exists():
                        shutil.copy(BOOKS_BACKUP, BOOKS_FILE)
                    
                    if ISSUES_BACKUP.exists():
                        shutil.copy(ISSUES_BACKUP, ISSUES_FILE)
                    
                    if SETTINGS_BACKUP.exists():
                        shutil.copy(SETTINGS_BACKUP, SETTINGS_FILE)
                    
                    st.success(f"Backup '{selected_backup}' restored successfully")
                except Exception as e:
                    st.error(f"Restore failed: {str(e)}")
        else:
            st.info("No backups available")
    else:
        st.info("No backups available")