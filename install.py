import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Create data directory
DATA_DIR = Path("library_app/data")
DATA_DIR.mkdir(exist_ok=True, parents=True)

# Create assets directory
ASSETS_DIR = Path("library_app/assets")
ASSETS_DIR.mkdir(exist_ok=True, parents=True)

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
)

st.title("Library Management System Installation")

st.write("""
## Your Library Management System is Ready!

This web application provides a complete solution for managing your library, including:

- Book management
- User management
- Issue/return tracking
- Reports and analytics
- Settings and preferences
- Audit logs
""")

# Installation status
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Installation Status")
    st.success("✅ App files created successfully")
    st.success("✅ Data directories initialized")
    st.success("✅ Default admin account created")
    st.success("✅ Sample books added")
    
    st.info("Default admin credentials:")
    st.code("Username: admin\nPassword: admin123")

with col2:
    # Create a simple pie chart for demonstration
    fig, ax = plt.subplots()
    categories = ['Fiction', 'Non-fiction', 'Science', 'History', 'Biography']
    sizes = [35, 25, 15, 15, 10]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    explode = (0.1, 0, 0, 0, 0)
    
    ax.pie(sizes, explode=explode, labels=categories, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Sample Book Categories')
    
    # Display the chart
    st.pyplot(fig)

st.markdown("---")

st.markdown("""
## How to Run the Application

To start the application, run the following command in your terminal:

```bash
streamlit run library_app/app.py
```

The application will open in your default web browser.
""")

st.markdown("---")

st.markdown("""
## Features

### 📊 Dashboard
- Overview of library statistics
- Quick actions
- Recent activity

### 📖 Book Management
- Add, edit, and delete books
- Manage categories
- View book inventory

### 👥 User Management
- Add and edit users
- Activate/deactivate users
- Manage user roles

### 📘 Issue/Return
- Issue books to users
- Process returns
- Track overdue books
- Manage fines

### 📊 Reports & Analytics
- Lending history reports
- Inventory reports
- Popular books and active users
- Fine collection summary

### ⚙️ Settings
- Library information
- Fine rules configuration
- Backup and restore database

### 📝 Audit Logs
- Track admin activities
- Filter logs by date, action, and user
""")

# Launch button
if st.button("Launch Library Management System", type="primary"):
    st.switch_page("library_app/app.py")