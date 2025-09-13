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
    load_books, save_books, 
    load_users, save_users,
    sidebar_nav
)

# Set page configuration
st.set_page_config(
    page_title="Book Management",
    page_icon="📖",
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
st.title("Book Management")

# Tabs for different book operations
tab1, tab2, tab3, tab4 = st.tabs(["Book List", "Add Book", "Edit Book", "Categories"])

# Book List Tab
with tab1:
    st.header("Book List")
    books = load_books()
    
    # Search and filter
    search = st.text_input("Search books by title, author, or ISBN")
    
    # Filter books based on search
    if search:
        filtered_books = [book for book in books if 
                          search.lower() in book['title'].lower() or 
                          search.lower() in book['author'].lower() or 
                          search.lower() in book['isbn'].lower()]
    else:
        filtered_books = books
    
    # Convert to DataFrame for display
    if filtered_books:
        df = pd.DataFrame(filtered_books)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No books found")
    
    # Delete book functionality
    st.subheader("Delete Book")
    if books:
        book_ids = {book['title']: book['id'] for book in books}
        selected_book = st.selectbox("Select Book to Delete", list(book_ids.keys()))
        
        if st.button("Delete Book"):
            book_id = book_ids[selected_book]
            books = [book for book in books if book['id'] != book_id]
            save_books(books)
            st.success(f"Book '{selected_book}' deleted successfully")
            st.rerun()
    else:
        st.info("No books to delete")

# Add Book Tab
with tab2:
    st.header("Add New Book")
    
    title = st.text_input("Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["Fiction", "Non-fiction", "Science", "History", "Biography", "Children", "Other"])
    with col2:
        stock = st.number_input("Stock", min_value=1, value=1)
    
    if st.button("Add Book"):
        if title and author and isbn:
            books = load_books()
            
            # Generate new ID
            new_id = max([book['id'] for book in books], default=0) + 1
            
            # Create new book
            new_book = {
                'id': new_id,
                'title': title,
                'author': author,
                'isbn': isbn,
                'category': category,
                'stock': stock,
                'available': stock,
                'added_on': datetime.now().strftime('%Y-%m-%d')
            }
            
            books.append(new_book)
            save_books(books)
            
            st.success(f"Book '{title}' added successfully")
            st.rerun()
        else:
            st.error("Please fill in all required fields")

# Edit Book Tab
with tab3:
    st.header("Edit Book")
    
    books = load_books()
    
    if books:
        book_titles = {book['title']: book['id'] for book in books}
        selected_title = st.selectbox("Select Book to Edit", list(book_titles.keys()))
        selected_id = book_titles[selected_title]
        
        # Get selected book
        selected_book = next((book for book in books if book['id'] == selected_id), None)
        
        if selected_book:
            title = st.text_input("Title", value=selected_book['title'])
            author = st.text_input("Author", value=selected_book['author'])
            isbn = st.text_input("ISBN", value=selected_book['isbn'])
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Category", ["Fiction", "Non-fiction", "Science", "History", "Biography", "Children", "Other"], index=["Fiction", "Non-fiction", "Science", "History", "Biography", "Children", "Other"].index(selected_book['category']) if selected_book['category'] in ["Fiction", "Non-fiction", "Science", "History", "Biography", "Children", "Other"] else 0)
            with col2:
                stock = st.number_input("Stock", min_value=1, value=selected_book['stock'])
            
            if st.button("Update Book"):
                if title and author and isbn:
                    # Calculate books currently on loan
                    books_on_loan = selected_book['stock'] - selected_book['available']
                    
                    # Update book
                    selected_book['title'] = title
                    selected_book['author'] = author
                    selected_book['isbn'] = isbn
                    selected_book['category'] = category
                    selected_book['stock'] = stock
                    selected_book['available'] = max(0, stock - books_on_loan)
                    
                    # Save books
                    save_books(books)
                    
                    st.success(f"Book '{title}' updated successfully")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")
    else:
        st.info("No books to edit")

# Categories Tab
with tab4:
    st.header("Category Management")
    
    books = load_books()
    
    if books:
        # Count books by category
        categories = {}
        for book in books:
            if book['category'] in categories:
                categories[book['category']] += 1
            else:
                categories[book['category']] = 1
        
        # Display categories
        df = pd.DataFrame({'Category': list(categories.keys()), 'Book Count': list(categories.values())})
        st.dataframe(df, use_container_width=True)
        
        # Bulk category update
        st.subheader("Bulk Category Update")
        
        old_category = st.selectbox("Select Category to Update", list(categories.keys()))
        new_category = st.text_input("New Category Name")
        
        if st.button("Update Category"):
            if new_category:
                # Update books
                for book in books:
                    if book['category'] == old_category:
                        book['category'] = new_category
                
                # Save books
                save_books(books)
                
                st.success(f"Category '{old_category}' updated to '{new_category}' successfully")
                st.rerun()
            else:
                st.error("Please enter a new category name")
    else:
        st.info("No books available for category management")