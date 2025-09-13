import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

# Import from app.py
from app import (
    load_books, save_books,
    load_users, save_users,
    load_issues, save_issues,
    load_settings, save_settings,
    sidebar_nav
)

# Set page configuration
st.set_page_config(
    page_title="Issue/Return Management",
    page_icon="📘",
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
st.title("Issue/Return Management")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["Issue Book", "Return Book", "Current Issues", "Reservations"])

# Issue Book Tab
with tab1:
    st.header("Issue Book to User")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    settings = load_settings()
    
    # Filter available books and active users
    available_books = [book for book in books if book['available'] > 0]
    active_users = {k: v for k, v in users.items() if v['active'] and v['role'] == 'user'}
    
    if available_books and active_users:
        # Select user
        username_list = list(active_users.keys())
        selected_username = st.selectbox("Select User", username_list)
        
        # Count books already issued to this user
        user_issues = [issue for issue in issues if issue['username'] == selected_username and issue['return_date'] is None]
        max_books = settings['max_books_per_user']
        
        if len(user_issues) >= max_books:
            st.warning(f"User has already reached the maximum limit of {max_books} books")
        else:
            st.write(f"User has {len(user_issues)} books out of {max_books} maximum")
            
            # Select book
            book_titles = {book['title']: book['id'] for book in available_books}
            selected_title = st.selectbox("Select Book", list(book_titles.keys()))
            selected_book_id = book_titles[selected_title]
            
            # Set issue date and expected return date
            issue_date = st.date_input("Issue Date", datetime.now())
            loan_period = settings['loan_period_days']
            expected_return = issue_date + timedelta(days=loan_period)
            st.write(f"Expected Return Date: {expected_return.strftime('%Y-%m-%d')}")
            
            if st.button("Issue Book"):
                # Update book availability
                for book in books:
                    if book['id'] == selected_book_id:
                        book['available'] -= 1
                        break
                
                # Create new issue record
                new_issue = {
                    'username': selected_username,
                    'book_id': selected_book_id,
                    'issue_date': issue_date.strftime('%Y-%m-%d'),
                    'expected_return_date': expected_return.strftime('%Y-%m-%d'),
                    'return_date': None,
                    'fine_paid': 0.0,
                    'status': 'issued'
                }
                
                issues.append(new_issue)
                
                # Save data
                save_books(books)
                save_issues(issues)
                
                st.success(f"Book '{selected_title}' issued to {selected_username} successfully")
                st.rerun()
    else:
        if not available_books:
            st.warning("No books available to issue")
        if not active_users:
            st.warning("No active users to issue books to")

# Return Book Tab
with tab2:
    st.header("Return Book")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    settings = load_settings()
    
    # Filter current issues
    current_issues = [issue for issue in issues if issue['return_date'] is None]
    
    if current_issues:
        # Create a readable list of issues for selection
        issue_options = []
        issue_map = {}
        
        for i, issue in enumerate(current_issues):
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            user = users.get(issue['username'], None)
            
            if book and user:
                option = f"{user['first_name']} {user['last_name']} - {book['title']} (Issued: {issue['issue_date']})"
                issue_options.append(option)
                issue_map[option] = i
        
        selected_issue_option = st.selectbox("Select Issue to Return", issue_options)
        selected_issue_index = issue_map[selected_issue_option]
        issue = current_issues[selected_issue_index]
        
        # Get book and user details
        book = next((b for b in books if b['id'] == issue['book_id']), None)
        user = users.get(issue['username'], None)
        
        if book and user:
            st.write(f"Book: {book['title']}")
            st.write(f"User: {user['first_name']} {user['last_name']}")
            st.write(f"Issue Date: {issue['issue_date']}")
            st.write(f"Expected Return Date: {issue['expected_return_date']}")
            
            # Calculate fine if overdue
            return_date = st.date_input("Return Date", datetime.now())
            expected_return_date = datetime.strptime(issue['expected_return_date'], '%Y-%m-%d').date()
            
            if return_date > expected_return_date:
                days_overdue = (return_date - expected_return_date).days
                fine_rate = settings['fine_per_day']
                fine_amount = days_overdue * fine_rate
                
                st.warning(f"Book is overdue by {days_overdue} days")
                st.write(f"Fine Amount: ${fine_amount:.2f}")
                
                fine_paid = st.number_input("Fine Paid", min_value=0.0, max_value=float(fine_amount), value=float(fine_amount), step=0.5)
            else:
                fine_paid = 0.0
            
            if st.button("Return Book"):
                # Update issue record
                issue['return_date'] = return_date.strftime('%Y-%m-%d')
                issue['fine_paid'] = fine_paid
                issue['status'] = 'returned'
                
                # Update book availability
                for b in books:
                    if b['id'] == book['id']:
                        b['available'] += 1
                        break
                
                # Save data
                save_books(books)
                save_issues(issues)
                
                st.success(f"Book '{book['title']}' returned successfully")
                st.rerun()
    else:
        st.info("No books currently issued")

# Current Issues Tab
with tab3:
    st.header("Current Issues")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    settings = load_settings()
    
    # Filter current issues
    current_issues = [issue for issue in issues if issue['return_date'] is None]
    
    if current_issues:
        # Create list for DataFrame
        issues_list = []
        
        for issue in current_issues:
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            user = users.get(issue['username'], None)
            
            if book and user:
                # Calculate days until due or overdue
                today = datetime.now().date()
                expected_return_date = datetime.strptime(issue['expected_return_date'], '%Y-%m-%d').date()
                days_diff = (expected_return_date - today).days
                
                status = "Overdue" if days_diff < 0 else "Due"
                days_text = f"{abs(days_diff)} days {'overdue' if days_diff < 0 else 'left'}"
                
                issues_list.append({
                    'User': f"{user['first_name']} {user['last_name']}",
                    'Book': book['title'],
                    'Issue Date': issue['issue_date'],
                    'Due Date': issue['expected_return_date'],
                    'Status': status,
                    'Days': days_text
                })
        
        # Convert to DataFrame and display
        df = pd.DataFrame(issues_list)
        st.dataframe(df, use_container_width=True)
        
        # Overdue items summary
        overdue_issues = [i for i in issues_list if i['Status'] == 'Overdue']
        if overdue_issues:
            st.subheader("Overdue Summary")
            st.warning(f"{len(overdue_issues)} books are currently overdue")
            
            # Display overdue books
            df_overdue = pd.DataFrame(overdue_issues)
            st.dataframe(df_overdue, use_container_width=True)
    else:
        st.info("No books currently issued")

# Reservations Tab
with tab4:
    st.header("Book Reservations")
    st.info("This feature is currently under development")
    
    # Placeholder for reservation functionality
    st.write("Coming soon: Book reservation system")
    st.write("Features will include:")
    st.write("- Request a book that is currently checked out")
    st.write("- Queue management for popular books")
    st.write("- Notification system for when a book becomes available")
    st.write("- Reservation expiration and management")