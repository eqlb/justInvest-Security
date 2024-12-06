import os
import re
from hashlib import blake2b
import secrets
# Kyle Taticek 101193550
# Constants
ACCESS_CONTROL_POLICY = {
    "Client": [1, 2, 4],
    "Premium Client": [1, 2, 3, 4, 5],
    "Financial Advisor": [1, 2, 3, 7],
    "Financial Planner": [1, 2, 3, 6, 7],
    "Teller": [1, 2]
}

BUSINESS_DAY_START_HOUR = 9
BUSINESS_DAY_CLOSE_HOUR = 17

FILENAME = "passwd.txt"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE_PATH = os.path.join(SCRIPT_PATH, FILENAME)

# List of weak passwords
WEAK_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "abc123", "password1", "1234", "1234567", "passw0rd"
]

# Functions
#Problem 2 c: Hash Function Implmentation
def hash_password(password, salt=None):
    """Hashes a password using blake2b and a salt."""
    if not salt:
        salt = secrets.token_bytes(16)
    hash_obj = blake2b(password.encode('utf-8'), salt=salt, digest_size=32)
    return hash_obj.hexdigest(), salt


def verify_password(stored_hash, entered_password, salt):
    """Verifies a password by rehashing with the stored salt."""
    entered_hash, _ = hash_password(entered_password, salt=salt)
    return entered_hash == stored_hash

# Problem 2 c: Password File Management
def write_user_to_file(username, hashed_password, salt, role):
    """Writes a user's credentials and role to the password file."""
    with open(PASSWORD_FILE_PATH, "a") as file:
        file.write(f"{username},{hashed_password},{salt.hex()},{role}\n")


def check_file_for_user(entered_username):
    """Checks if a user exists in the password file and returns their details."""
    if not os.path.exists(PASSWORD_FILE_PATH):
        return None
    with open(PASSWORD_FILE_PATH, "r") as file:
        for line in file:
            entry = line.strip().split(",")
            if len(entry) != 4:  # Ensure the line has exactly 4 fields
                continue
            username, stored_hash, salt, role = entry
            if username.lower() == entered_username.lower():
                return stored_hash, bytes.fromhex(salt), role
    return None



def valid_username(username):
    """Checks if a username exists in passwd.txt."""
    if not os.path.exists(PASSWORD_FILE_PATH):
        return False
    with open(PASSWORD_FILE_PATH, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if stored_username.lower() == username.lower():
                return True
    return False

# Problem 3 b: Proactive Password Checker
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

# Problem 3 a: User Signup Interface
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

# Problem 4 a & b: Login and Access Rights
def authenticate_user(username):
    """Authenticates a user by checking their password and displays access rights."""
    user_record = check_file_for_user(username)
    if not user_record:
        print("User not found.")
        return False, None
    stored_hash, salt, role = user_record
    password = input("Please enter your password: ").strip()
    if verify_password(stored_hash, password, salt):
        print("ACCESS GRANTED!")
        print(f"Welcome, {username}! You are logged in as a {role}.")
        display_access_rights(role)
        return True, role
    print("Invalid password.")
    return False, None

# Problem 4 b: Display Access Rights
def display_access_rights(role):
    """Displays the operations available to the user based on their role."""
    operations = {
        1: "View account balance",
        2: "View investment portfolio",
        3: "Modify investment portfolio",
        4: "View Financial Advisor contact info",
        5: "View Financial Planner contact info",
        6: "View money market instruments",
        7: "View private consumer instruments"
    }
    if role not in ACCESS_CONTROL_POLICY:
        print("Role not recognized. No operations available.")
        return

    allowed_operations = ACCESS_CONTROL_POLICY[role]
    print("You have access to the following operations:")
    for op in allowed_operations:
        print(f"{op}. {operations[op]}")




def print_operations():
    """Prints available operations."""
    print("Operations available on the system:")
    print("1. View account balance")
    print("2. View investment portfolio")
    print("3. Modify investment portfolio")
    print("4. View Financial Advisor contact info")
    print("5. View Financial Planner contact info")
    print("6. View money market instruments")
    print("7. View private consumer instruments")
    print()

# Problem 1 c: Business Hours Restriction
def set_time():
    """Sets the time and checks if a Teller can access the system."""
    while True:
        try:
            time = int(input("Please enter the hour of the day (use 24-hour notation): "))
            if 0 <= time <= 23:
                if accessible_to_teller(time):
                    print("System accessible during business hours.")
                    return True
                else:
                    print("System is inaccessible outside business hours. Goodbye!")
                    return False
            else:
                print("Invalid hour. Please enter a number between 0 and 23.")
        except ValueError:
            print("Invalid input. Please enter a valid hour.")


def accessible_to_teller(time):
    """Checks if a Teller has access based on the time."""
    return BUSINESS_DAY_START_HOUR <= time < BUSINESS_DAY_CLOSE_HOUR


def user_sign_in(teller_access):
    """Handles user sign-in."""
    while True:
        username = input("Enter username to sign in or 0 to register: ").strip()
        if username == "0":
            launch_signup()
        elif valid_username(username):
            authenticated, role = authenticate_user(username)
            if authenticated:
                if role == "Teller" and not teller_access:
                    print("Teller can't access the system outside of business hours!")
                    continue
                return role
        else:
            print("Invalid username. Please try again.")


def user_selection():
    """Handles user operation selection."""
    while True:
        try:
            return int(input("Which operation would you like to perform? Enter 0 to quit.\n"))
        except ValueError:
            print("Invalid input. Please enter a number.")

# Problem 1 c: Access Control Implementation
def access_control(user_select, user_role):
    """Implements access control for user operations."""
    operations = {
        1: "View account balance",
        2: "View investment portfolio",
        3: "Modify investment portfolio",
        4: "View Financial Advisor contact info",
        5: "View Financial Planner contact info",
        6: "View money market instruments",
        7: "View private consumer instruments"
    }
    
    if user_role not in ACCESS_CONTROL_POLICY or user_select not in ACCESS_CONTROL_POLICY[user_role]:
        print("Access Denied!")
    else:
        print(f"Performing operation: {operations[user_select]}")


#Problem 4
def main():
    """Main function."""
    print("Welcome to justInvest System")
    teller_access = set_time()

    # Exit if access is denied for all users (including Tellers)
    if not teller_access:
        return

    # Continue if access is granted
    print_operations()
    user_role = user_sign_in(teller_access)
    while True:
        user_select = user_selection()
        if user_select == 0:
            print("Goodbye!")
            break
        access_control(user_select, user_role)



# Main program
if __name__ == '__main__':
    main()
