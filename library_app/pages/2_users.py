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
    load_users, save_users,
    sidebar_nav
)

# Set page configuration
st.set_page_config(
    page_title="User Management",
    page_icon="👥",
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
st.title("User Management")

# Tabs for different user operations
tab1, tab2, tab3 = st.tabs(["User List", "Add User", "Edit User"])

# User List Tab
with tab1:
    st.header("User List")
    users = load_users()
    
    # Search and filter
    search = st.text_input("Search users by name or email")
    
    # Filter users based on search
    if search:
        filtered_users = {k: v for k, v in users.items() if 
                          search.lower() in v['first_name'].lower() or 
                          search.lower() in v['last_name'].lower() or 
                          search.lower() in v['email'].lower()}
    else:
        filtered_users = users
    
    # Convert to DataFrame for display
    if filtered_users:
        # Create list of dictionaries for DataFrame
        users_list = []
        for username, user in filtered_users.items():
            user_dict = {
                'Username': username,
                'Name': f"{user['first_name']} {user['last_name']}",
                'Email': user['email'],
                'Role': user['role'].capitalize(),
                'Status': 'Active' if user['active'] else 'Inactive',
                'Created': user['created_at']
            }
            users_list.append(user_dict)
        
        df = pd.DataFrame(users_list)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found")
    
    # Activate/Deactivate user functionality
    st.subheader("Activate/Deactivate User")
    if users:
        username_list = list(users.keys())
        selected_user = st.selectbox("Select User", username_list)
        
        is_active = users[selected_user]['active']
        if is_active:
            if st.button("Deactivate User"):
                users[selected_user]['active'] = False
                save_users(users)
                st.success(f"User '{selected_user}' deactivated successfully")
                st.rerun()
        else:
            if st.button("Activate User"):
                users[selected_user]['active'] = True
                save_users(users)
                st.success(f"User '{selected_user}' activated successfully")
                st.rerun()
    else:
        st.info("No users to manage")

# Add User Tab
with tab2:
    st.header("Add New User")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
    with col2:
        last_name = st.text_input("Last Name")
    
    email = st.text_input("Email")
    role = st.selectbox("Role", ["admin", "user"])
    
    if st.button("Add User"):
        if username and password and first_name and last_name and email:
            users = load_users()
            
            if username in users:
                st.error(f"Username '{username}' already exists")
            else:
                # Create new user
                new_user = {
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'role': role,
                    'active': True,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                users[username] = new_user
                save_users(users)
                
                st.success(f"User '{username}' added successfully")
                st.rerun()
        else:
            st.error("Please fill in all required fields")

# Edit User Tab
with tab3:
    st.header("Edit User")
    
    users = load_users()
    
    if users:
        username_list = list(users.keys())
        selected_user = st.selectbox("Select User to Edit", username_list)
        
        # Get selected user
        user = users[selected_user]
        
        change_password = st.checkbox("Change Password")
        if change_password:
            password = st.text_input("New Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user['first_name'])
        with col2:
            last_name = st.text_input("Last Name", value=user['last_name'])
        
        email = st.text_input("Email", value=user['email'])
        role = st.selectbox("Role", ["admin", "user"], index=0 if user['role'] == 'admin' else 1)
        
        if st.button("Update User"):
            if first_name and last_name and email:
                # Update user
                user['first_name'] = first_name
                user['last_name'] = last_name
                user['email'] = email
                user['role'] = role
                
                if change_password and password:
                    user['password'] = password
                
                # Save users
                save_users(users)
                
                st.success(f"User '{selected_user}' updated successfully")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    else:
        st.info("No users to edit")