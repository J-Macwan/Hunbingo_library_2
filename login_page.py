# Import the tkinter library - this is for making GUI applications
import tkinter as tk
# Import messagebox for showing pop-up messages
from tkinter import messagebox

# Step 1: Create our login window
window = tk.Tk()
window.title("My First Login Page")  # Set the window title
window.geometry("500x400")  # Set the window size (width x height)
window.configure(bg="#f0f0f0")  # Light gray background

# Step 2: Create a heading for our login page
heading = tk.Label(window, text="User Registration", font=("Arial", 16, "bold"), bg="#f0f0f0")
heading.pack(pady=15)  # Add some padding around the heading

# Step 3: Create input fields with labels
# First Name
tk.Label(window, text="First Name:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=80)
first_name_entry = tk.Entry(window, width=40)
first_name_entry.pack(pady=5)

# Last Name
tk.Label(window, text="Last Name:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=80)
last_name_entry = tk.Entry(window, width=40)
last_name_entry.pack(pady=5)

# Email
tk.Label(window, text="Email:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=80)
email_entry = tk.Entry(window, width=40)
email_entry.pack(pady=5)

# Password - using show="*" to hide the password characters
tk.Label(window, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=80)
password_entry = tk.Entry(window, width=40, show="*")  # The * hides the actual characters
password_entry.pack(pady=5)

# Confirm Password
tk.Label(window, text="Confirm Password:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", padx=80)
confirm_password_entry = tk.Entry(window, width=40, show="*")
confirm_password_entry.pack(pady=5)

# Step 4: Create a function that runs when the Login button is clicked
def login():
    # Get the text from each entry field
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    
    # Check if any field is empty
    if first_name == "" or last_name == "" or email == "" or password == "" or confirm_password == "":
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    
    # If everything is ok, show success message
    messagebox.showinfo("Success", f"Welcome, {first_name} {last_name}!")
    
# Step 5: Create a Login button
login_button = tk.Button(
    window, 
    text="Register", 
    command=login,  # Link to the login function
    bg="#4CAF50",  # Green button
    fg="white",    # White text
    width=15,
    height=2
)
login_button.pack(pady=20)

# Step 6: Start the program
# This line starts the main loop that keeps the window open
window.mainloop()