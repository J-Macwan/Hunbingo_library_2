import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from pathlib import Path

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
    page_title="Reports & Analytics",
    page_icon="📊",
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
st.title("Reports & Analytics")

# Tabs for different reports
tab1, tab2, tab3, tab4 = st.tabs(["Lending History", "Inventory", "Popular Books", "Fine Collection"])

# Lending History Tab
with tab1:
    st.header("Lending History Report")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    
    # Date filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # User filter
    username_list = ["All Users"] + list(users.keys())
    selected_user = st.selectbox("Select User", username_list)
    
    # Book filter
    book_titles = ["All Books"] + [book['title'] for book in books]
    selected_book = st.selectbox("Select Book", book_titles)
    
    # Filter issues based on selection
    filtered_issues = []
    
    for issue in issues:
        issue_date = datetime.strptime(issue['issue_date'], '%Y-%m-%d').date()
        
        # Check date range
        if start_date <= issue_date <= end_date:
            # Check user filter
            if selected_user == "All Users" or issue['username'] == selected_user:
                # Check book filter
                book = next((b for b in books if b['id'] == issue['book_id']), None)
                if book and (selected_book == "All Books" or book['title'] == selected_book):
                    filtered_issues.append(issue)
    
    if filtered_issues:
        # Create list for DataFrame
        issues_list = []
        
        for issue in filtered_issues:
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            user = users.get(issue['username'], None)
            
            if book and user:
                issues_list.append({
                    'User': f"{user['first_name']} {user['last_name']}",
                    'Book': book['title'],
                    'Issue Date': issue['issue_date'],
                    'Return Date': issue['return_date'] if issue['return_date'] else "Not Returned",
                    'Status': issue['status'].capitalize(),
                    'Fine Paid': f"${issue['fine_paid']:.2f}" if issue['fine_paid'] else "$0.00"
                })
        
        # Convert to DataFrame and display
        df = pd.DataFrame(issues_list)
        st.dataframe(df, use_container_width=True)
        
        # Download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Report as CSV",
            csv,
            "lending_history_report.csv",
            "text/csv",
            key='download-csv'
        )
        
        # Summary statistics
        st.subheader("Summary Statistics")
        st.write(f"Total Records: {len(filtered_issues)}")
        st.write(f"Books Returned: {len([i for i in filtered_issues if i['return_date'] is not None])}")
        st.write(f"Books Still Out: {len([i for i in filtered_issues if i['return_date'] is None])}")
        
        # Calculate total fines
        total_fines = sum(issue['fine_paid'] for issue in filtered_issues if issue['fine_paid'])
        st.write(f"Total Fines Collected: ${total_fines:.2f}")
    else:
        st.info("No lending history found for the selected filters")

# Inventory Tab
with tab2:
    st.header("Inventory Report")
    
    # Load data
    books = load_books()
    issues = load_issues()
    
    if books:
        # Create inventory DataFrame
        inventory_list = []
        
        for book in books:
            inventory_list.append({
                'Title': book['title'],
                'Author': book['author'],
                'Category': book['category'],
                'Total Stock': book['stock'],
                'Available': book['available'],
                'Checked Out': book['stock'] - book['available'],
                'Added On': book['added_on']
            })
        
        # Convert to DataFrame and display
        df = pd.DataFrame(inventory_list)
        st.dataframe(df, use_container_width=True)
        
        # Inventory summary
        st.subheader("Inventory Summary")
        total_books = sum(book['stock'] for book in books)
        available_books = sum(book['available'] for book in books)
        checked_out = total_books - available_books
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", total_books)
        with col2:
            st.metric("Available Books", available_books)
        with col3:
            st.metric("Checked Out", checked_out)
        
        # Category breakdown chart
        st.subheader("Books by Category")
        category_counts = {}
        
        for book in books:
            if book['category'] in category_counts:
                category_counts[book['category']] += book['stock']
            else:
                category_counts[book['category']] = book['stock']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.pie(
            category_counts.values(), 
            labels=category_counts.keys(), 
            autopct='%1.1f%%',
            startangle=90
        )
        plt.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No books in inventory")

# Popular Books Tab
with tab3:
    st.header("Popular Books & Active Users")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    
    if issues:
        # Calculate book popularity
        book_popularity = {}
        
        for issue in issues:
            if issue['book_id'] in book_popularity:
                book_popularity[issue['book_id']] += 1
            else:
                book_popularity[issue['book_id']] = 1
        
        # Get book titles for popular books
        popular_books = []
        
        for book_id, count in book_popularity.items():
            book = next((b for b in books if b['id'] == book_id), None)
            if book:
                popular_books.append({
                    'Title': book['title'],
                    'Author': book['author'],
                    'Category': book['category'],
                    'Times Borrowed': count
                })
        
        # Sort by popularity
        popular_books = sorted(popular_books, key=lambda x: x['Times Borrowed'], reverse=True)
        
        # Display popular books
        st.subheader("Most Popular Books")
        df_popular = pd.DataFrame(popular_books)
        st.dataframe(df_popular, use_container_width=True)
        
        # Bar chart of popular books (top 10)
        if popular_books:
            top_books = popular_books[:10] if len(popular_books) > 10 else popular_books
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(
                x=[book['Times Borrowed'] for book in top_books],
                y=[book['Title'] for book in top_books],
                palette='viridis'
            )
            plt.xlabel('Times Borrowed')
            plt.ylabel('Book Title')
            plt.title('Top 10 Most Popular Books')
            st.pyplot(fig)
        
        # Calculate active users
        user_activity = {}
        
        for issue in issues:
            if issue['username'] in user_activity:
                user_activity[issue['username']] += 1
            else:
                user_activity[issue['username']] = 1
        
        # Get user details for active users
        active_users = []
        
        for username, count in user_activity.items():
            user = users.get(username, None)
            if user:
                active_users.append({
                    'Name': f"{user['first_name']} {user['last_name']}",
                    'Email': user['email'],
                    'Books Borrowed': count
                })
        
        # Sort by activity
        active_users = sorted(active_users, key=lambda x: x['Books Borrowed'], reverse=True)
        
        # Display active users
        st.subheader("Most Active Users")
        df_active = pd.DataFrame(active_users)
        st.dataframe(df_active, use_container_width=True)
    else:
        st.info("No lending history available for analysis")

# Fine Collection Tab
with tab4:
    st.header("Fine Collection Summary")
    
    # Load data
    books = load_books()
    users = load_users()
    issues = load_issues()
    
    # Filter issues with fines
    fined_issues = [issue for issue in issues if issue['fine_paid'] and issue['fine_paid'] > 0]
    
    if fined_issues:
        # Create list for DataFrame
        fines_list = []
        
        for issue in fined_issues:
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            user = users.get(issue['username'], None)
            
            if book and user:
                issue_date = datetime.strptime(issue['issue_date'], '%Y-%m-%d')
                return_date = datetime.strptime(issue['return_date'], '%Y-%m-%d') if issue['return_date'] else datetime.now()
                days_kept = (return_date - issue_date).days
                
                fines_list.append({
                    'User': f"{user['first_name']} {user['last_name']}",
                    'Book': book['title'],
                    'Issue Date': issue['issue_date'],
                    'Return Date': issue['return_date'] if issue['return_date'] else "Not Returned",
                    'Days Kept': days_kept,
                    'Fine Amount': f"${issue['fine_paid']:.2f}"
                })
        
        # Convert to DataFrame and display
        df = pd.DataFrame(fines_list)
        st.dataframe(df, use_container_width=True)
        
        # Calculate total fines
        total_fines = sum(issue['fine_paid'] for issue in fined_issues)
        
        # Fine summary
        st.subheader("Fine Summary")
        st.metric("Total Fines Collected", f"${total_fines:.2f}")
        st.metric("Number of Overdue Returns", len(fined_issues))
        
        if len(fined_issues) > 0:
            avg_fine = total_fines / len(fined_issues)
            st.metric("Average Fine Amount", f"${avg_fine:.2f}")
        
        # Monthly fine collection chart
        st.subheader("Monthly Fine Collection")
        
        # Group fines by month
        monthly_fines = {}
        
        for issue in fined_issues:
            if issue['return_date']:
                month = datetime.strptime(issue['return_date'], '%Y-%m-%d').strftime('%Y-%m')
                
                if month in monthly_fines:
                    monthly_fines[month] += issue['fine_paid']
                else:
                    monthly_fines[month] = issue['fine_paid']
        
        if monthly_fines:
            # Sort months
            sorted_months = sorted(monthly_fines.keys())
            
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))
            plt.bar(
                sorted_months,
                [monthly_fines[month] for month in sorted_months],
                color='crimson'
            )
            plt.xlabel('Month')
            plt.ylabel('Fine Amount ($)')
            plt.title('Monthly Fine Collection')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    else:
        st.info("No fines have been collected")