import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import pickle
import random
from pathlib import Path

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'role' not in st.session_state:
    st.session_state['role'] = None

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths for data files
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.pkl"
BOOKS_FILE = DATA_DIR / "books.pkl"
ISSUES_FILE = DATA_DIR / "issues.pkl"
SETTINGS_FILE = DATA_DIR / "settings.pkl"

# Create initial data if it doesn't exist
def initialize_data():
    # Default admin user
    if not USERS_FILE.exists():
        users = {
            'admin': {
                'password': 'admin123',
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@library.com',
                'role': 'admin',
                'active': True,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        with open(USERS_FILE, 'wb') as f:
            pickle.dump(users, f)
    
    # Sample books
    if not BOOKS_FILE.exists():
        books = [
            {
                'id': 1,
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'category': 'Fiction',
                'stock': 5,
                'available': 5,
                'added_on': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'id': 2,
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'category': 'Fiction',
                'stock': 3,
                'available': 3,
                'added_on': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'id': 3,
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'category': 'Fiction',
                'stock': 4,
                'available': 4,
                'added_on': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        with open(BOOKS_FILE, 'wb') as f:
            pickle.dump(books, f)
    
    # Sample issues
    if not ISSUES_FILE.exists():
        issues = []
        with open(ISSUES_FILE, 'wb') as f:
            pickle.dump(issues, f)
    
    # Default settings
    if not SETTINGS_FILE.exists():
        settings = {
            'library_name': 'Central Library',
            'contact_email': 'contact@library.com',
            'contact_phone': '123-456-7890',
            'operating_hours': '9:00 AM - 6:00 PM',
            'fine_per_day': 1.00,
            'max_books_per_user': 5,
            'loan_period_days': 14
        }
        with open(SETTINGS_FILE, 'wb') as f:
            pickle.dump(settings, f)

# Initialize data
initialize_data()

# Load data functions
def load_users():
    with open(USERS_FILE, 'rb') as f:
        return pickle.load(f)

def load_books():
    with open(BOOKS_FILE, 'rb') as f:
        return pickle.load(f)

def load_issues():
    with open(ISSUES_FILE, 'rb') as f:
        return pickle.load(f)

def load_settings():
    with open(SETTINGS_FILE, 'rb') as f:
        return pickle.load(f)

# Save data functions
def save_users(users):
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users, f)

def save_books(books):
    with open(BOOKS_FILE, 'wb') as f:
        pickle.dump(books, f)

def save_issues(issues):
    with open(ISSUES_FILE, 'wb') as f:
        pickle.dump(issues, f)

def save_settings(settings):
    with open(SETTINGS_FILE, 'wb') as f:
        pickle.dump(settings, f)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #343a40;
    }
    h1, h2, h3 {
        color: #2C3E50;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .dashboard-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .dashboard-card h3 {
        margin-top: 0;
    }
    .dashboard-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Login function
def login(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password and users[username]['active']:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['role'] = users[username]['role']
        return True
    return False

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None

# Sidebar navigation
def sidebar_nav():
    settings = load_settings()
    st.sidebar.title(f"📚 {settings['library_name']}")
    
    if st.session_state['logged_in']:
        users = load_users()
        user = users[st.session_state['username']]
        st.sidebar.write(f"Welcome, {user['first_name']} {user['last_name']}")
        st.sidebar.write(f"Role: {user['role'].capitalize()}")
        
        st.sidebar.markdown("---")
        
        st.sidebar.header("Navigation")
        st.sidebar.page_link("library_app/app.py", label="📊 Dashboard", icon="🏠")
        
        if st.session_state['role'] == 'admin':
            st.sidebar.page_link("library_app/pages/1_books.py", label="📖 Book Management", icon="📖")
            st.sidebar.page_link("library_app/pages/2_users.py", label="👥 User Management", icon="👥")
            st.sidebar.page_link("library_app/pages/3_issues.py", label="📘 Issue/Return", icon="📘")
            st.sidebar.page_link("library_app/pages/4_reports.py", label="📊 Reports & Analytics", icon="📊")
            st.sidebar.page_link("library_app/pages/5_settings.py", label="⚙️ Settings", icon="⚙️")
            st.sidebar.page_link("library_app/pages/6_audit.py", label="📝 Audit Logs", icon="📝")
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()

# Main content
def main_content():
    if not st.session_state['logged_in']:
        # Login page
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.title("Library Management System")
        st.markdown("Please login to continue")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login_button = st.button("Login")
        
        if login_button:
            if login(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Dashboard content
        st.title("Library Dashboard")
        
        books = load_books()
        users = load_users()
        issues = load_issues()
        
        # Filter active users
        active_users = {k: v for k, v in users.items() if v['active']}
        
        # Calculate books on loan
        books_on_loan = sum(book['stock'] - book['available'] for book in books)
        
        # Calculate overdue books
        today = datetime.now().date()
        settings = load_settings()
        loan_period = settings['loan_period_days']
        overdue_issues = [issue for issue in issues if issue['return_date'] is None and 
                         (today - datetime.strptime(issue['issue_date'], '%Y-%m-%d').date()).days > loan_period]
        
        # Display statistics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Total Books</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='dashboard-number'>{len(books)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Active Users</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='dashboard-number'>{len(active_users)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Books on Loan</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='dashboard-number'>{books_on_loan}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Overdue Books</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='dashboard-number'>{len(overdue_issues)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Recent activity
        st.markdown("### Recent Activity")
        
        if not issues:
            st.info("No recent activity")
        else:
            # Sort issues by date (most recent first)
            recent_issues = sorted(issues, key=lambda x: datetime.strptime(x['issue_date'], '%Y-%m-%d'), reverse=True)[:5]
            
            # Display recent issues
            for issue in recent_issues:
                book = next((b for b in books if b['id'] == issue['book_id']), None)
                user = users.get(issue['username'], None)
                
                if book and user:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{user['first_name']} {user['last_name']}** {issue['status']} **{book['title']}**")
                    with col2:
                        st.write(f"Date: {issue['issue_date']}")
                    st.markdown("---")
        
        # Quick actions
        st.markdown("### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Add New Book"):
                st.switch_page("library_app/pages/1_books.py")
        
        with col2:
            if st.button("Issue/Return Book"):
                st.switch_page("library_app/pages/3_issues.py")
        
        with col3:
            if st.button("View Reports"):
                st.switch_page("library_app/pages/4_reports.py")

# Display sidebar and main content
sidebar_nav()
main_content()