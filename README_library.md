# Library Management System

A complete web-based Library Management System built with Streamlit that runs in your browser.

## Features

- **Admin Dashboard**: Overview of library statistics, quick actions, and recent activity
- **Book Management**: Add, edit, delete books, manage categories
- **User Management**: User registration, account management, role-based access control
- **Issue/Return System**: Issue books to users, process returns, handle reservations
- **Reports & Analytics**: Generate reports on lending history, inventory, popular books
- **Settings & Preferences**: Configure library info, fine rules, backup/restore
- **Audit Logs**: Track admin activities for security and accountability

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required packages:

```bash
pip install streamlit matplotlib pandas seaborn
```

## Running the Application

To start the application, run:

```bash
streamlit run install.py
```

This will open the installation page in your browser. From there, you can launch the full application.

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Running in GitHub Codespace

This application is designed to run in a GitHub Codespace environment. When running in a Codespace:

1. The application will start a web server
2. You can access the web interface through your browser
3. All data is stored in the Codespace environment

## Data Storage

All library data is stored in the `library_app/data` directory using pickle files:

- `users.pkl`: User accounts and information
- `books.pkl`: Book inventory and details
- `issues.pkl`: Book issue/return records
- `settings.pkl`: Library settings and preferences
- `audit_logs.pkl`: System activity logs

## License

This project is provided as-is for educational purposes.

## Support

For questions or issues, please open an issue in the GitHub repository.