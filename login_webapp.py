import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Login Page",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2C3E50;
        text-align: center;
    }
    .description {
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.title("Welcome to Our Portal")
st.markdown('<p class="description">Please register to continue</p>', unsafe_allow_html=True)

# Create a form
with st.form("login_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", placeholder="Enter your first name")
    
    with col2:
        last_name = st.text_input("Last Name", placeholder="Enter your last name")
    
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    
    col3, col4 = st.columns(2)
    with col3:
        password = st.text_input("Password", type="password", placeholder="Create a password")
    with col4:
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")
    
    # Terms and conditions checkbox
    terms_agree = st.checkbox("I agree to the Terms and Conditions")
    
    # Submit button
    submit_button = st.form_submit_button("Register")

# Form validation
if submit_button:
    if not all([first_name, last_name, email, password, confirm_password]):
        st.error("⚠️ Please fill in all fields")
    elif not "@" in email or not "." in email:
        st.error("⚠️ Please enter a valid email address")
    elif password != confirm_password:
        st.error("⚠️ Passwords do not match")
    elif not terms_agree:
        st.error("⚠️ You must agree to the Terms and Conditions")
    else:
        # Success message
        st.success(f"✅ Welcome, {first_name}! Your account has been created successfully.")
        st.balloons()  # Fun animation for successful registration
        
        # Display account information
        st.subheader("Account Information")
        st.info(f"""
        **Name**: {first_name} {last_name}
        **Email**: {email}
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>© 2025 My Website. All rights reserved.</div>", 
    unsafe_allow_html=True
)