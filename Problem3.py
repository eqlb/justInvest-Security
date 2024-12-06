from Problem2 import hash_password, write_user_to_file, valid_username
from Problem1 import ACCESS_CONTROL_POLICY
import re
import os

# File path for weak passwords
WEAK_PASSWORDS_FILE = "weak_passwords.txt"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
WEAK_PASSWORDS_FILE_PATH = os.path.join(SCRIPT_PATH, WEAK_PASSWORDS_FILE)

# Load weak passwords
def load_weak_passwords(file_path):
    """Loads weak passwords from a file into a list."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Weak passwords file not found at {file_path}. Using an empty list.")
        return []
    except UnicodeDecodeError:
        print(f"Error reading {file_path}. Ensure the file is UTF-8 encoded.")
        return []

WEAK_PASSWORDS = load_weak_passwords(WEAK_PASSWORDS_FILE_PATH)

# Validate password function
def validate_password(username, password):
    """Validates a password against the defined rules."""
    errors = []
    if len(password) < 8 or len(password) > 12:
        errors.append("Password must be between 8 and 12 characters.")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must include at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("Password must include at least one lowercase letter.")
    if not re.search(r'\d', password):
        errors.append("Password must include at least one digit.")
    if not re.search(r'[!@#$%^&*]', password):
        errors.append("Password must include at least one special character (!, @, #, $, %, *, &).")
    if username.lower() in password.lower():
        errors.append("Password cannot include the username.")
    if password.lower() in WEAK_PASSWORDS:
        errors.append("Password is too common and weak.")

    if errors:
        print("\n".join(errors))
        return False
    return True

# User signup
def launch_signup():
    """Handles user signup."""
    username = input("Please enter your desired username: ").strip()
    if valid_username(username):
        print("Username already exists. Please try a different one.")
        return
    print("Available roles: Client, Premium Client, Financial Advisor, Financial Planner, Teller")
    role = input("Please select your role: ").strip()
    if role not in ACCESS_CONTROL_POLICY:
        print("Invalid role. Please try again.")
        return
    while True:
        password = input("Please enter your desired password: ").strip()
        if validate_password(username, password):
            break
    hashed_password, salt = hash_password(password)
    write_user_to_file(username, hashed_password, salt, role)
    print(f"User {username} successfully registered!")
