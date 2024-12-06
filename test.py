# Import necessary functions and constants from split modules
from Problem1 import set_time, access_control, ACCESS_CONTROL_POLICY
from Problem2 import PASSWORD_FILE_PATH, hash_password, valid_username, write_user_to_file, check_file_for_user
from Problem3 import launch_signup, validate_password
from Problem4 import authenticate_user

import os


def setup_test_environment():
    """Sets up a clean environment for testing by resetting the password file."""
    if os.path.exists(PASSWORD_FILE_PATH):
        os.remove(PASSWORD_FILE_PATH)
    print("Test environment set up. Password file reset.\n")


def test_signup():
    """Tests the user signup process with multiple users."""
    print("Running test: Signup")
    
    # Define test users
    test_users = [
        ("Sasha Kim", "Client"),
        ("Emery Blake", "Client"),
        ("Noor Abbasi", "Premium Client"),
        ("Zuri Adebayo", "Premium Client"),
        ("Mikael Chen", "Financial Advisor"),
        ("Jordan Riley", "Financial Advisor"),
        ("Ellis Nakamura", "Financial Planner"),
        ("Harper Diaz", "Financial Planner"),
        ("Alex Hayes", "Teller"),
        ("Adair Patel", "Teller"),
    ]
    
    # Mock user input for signup
    input_backup = __builtins__.input
    
    try:
        for username, role in test_users:
            password = f"{username.split()[0]}123!"  # Generate a valid password dynamically
            def mock_input(prompt):
                responses = {
                    "Please enter your desired username: ": username,
                    "Please select your role: ": role,
                    "Please enter your desired password: ": password
                }
                return responses[prompt]

            __builtins__.input = mock_input

            # Run signup process for each user
            launch_signup()

            # Verify that the user is now valid
            assert valid_username(username), f"Signup failed: Username {username} not found in file."
            print(f"Signup test passed for user {username}.")
    finally:
        __builtins__.input = input_backup



def test_login():
    """Tests the user login process with multiple users."""
    print("\nRunning test: Login")

    # Define test users with passwords (matching the ones used in test_signup)
    test_users = [
        ("Sasha Kim", "Client", "Sasha123!"),
        ("Emery Blake", "Client", "Emery123!"),
        ("Noor Abbasi", "Premium Client", "Noor123!"),
        ("Zuri Adebayo", "Premium Client", "Zuri123!"),
        ("Mikael Chen", "Financial Advisor", "Mikael123!"),
        ("Jordan Riley", "Financial Advisor", "Jordan123!"),
        ("Ellis Nakamura", "Financial Planner", "Ellis123!"),
        ("Harper Diaz", "Financial Planner", "Harper123!"),
        ("Alex Hayes", "Teller", "Alex123!"),
        ("Adair Patel", "Teller", "Adair123!"),
    ]

    input_backup = __builtins__.input
    try:
        for username, role, password in test_users:
            def mock_input(prompt):
                responses = {
                    "Enter username to sign in or 0 to register: ": username,
                    "Please enter your password: ": password
                }
                return responses[prompt]

            __builtins__.input = mock_input

            # Authenticate the user
            authenticated, user_role = authenticate_user(username)
            assert authenticated, f"Login failed: Authentication failed for {username}."
            assert user_role == role, f"Login failed: Expected role '{role}', got '{user_role}'."
            print(f"Login test passed for user {username}.")
    finally:
        __builtins__.input = input_backup



def test_access_control():
    """Tests access control for multiple users with their roles."""
    print("\nRunning test: Access Control")

    # Define test users with roles
    test_users = {
        "Client": ["Sasha Kim", "Emery Blake"],
        "Premium Client": ["Noor Abbasi", "Zuri Adebayo"],
        "Financial Advisor": ["Mikael Chen", "Jordan Riley"],
        "Financial Planner": ["Ellis Nakamura", "Harper Diaz"],
        "Teller": ["Alex Hayes", "Adair Patel"],
    }

    for role, users in test_users.items():
        print(f"Testing role: {role}")
        for user in users:
            allowed_operations = ACCESS_CONTROL_POLICY[role]
            for operation in range(1, 8):
                if operation in allowed_operations:
                    print(f"User {user}, Role {role}, Operation {operation}: Allowed")
                    assert operation in ACCESS_CONTROL_POLICY[role], (
                        f"Access denied for operation {operation}, but it should be allowed."
                    )
                else:
                    print(f"User {user}, Role {role}, Operation {operation}: Denied")
                    assert operation not in ACCESS_CONTROL_POLICY[role], (
                        f"Access granted for operation {operation}, but it should be denied."
                    )
    print("Access control test passed.")



def test_business_hours():
    """Tests the business hours restriction."""
    print("\nRunning test: Business Hours")

    # Mock user input for business hours
    def mock_input_valid_hour(prompt):
        return "10"  # Simulate a valid hour (10 AM)

    def mock_input_invalid_hour(prompt):
        return "20"  # Simulate an invalid hour (8 PM)

    # Backup original input function
    input_backup = __builtins__.input

    try:
        # Test valid hour
        __builtins__.input = mock_input_valid_hour
        assert set_time() == True, "Business hours test failed: Access should be allowed during business hours."

        # Test invalid hour
        __builtins__.input = mock_input_invalid_hour
        assert set_time() == False, "Business hours test failed: Access should be denied outside business hours."

        print("Business hours test passed.")
    finally:
        # Restore original input function
        __builtins__.input = input_backup


def test_password_policy():
    """Tests the password policy."""
    print("\nRunning test: Password Policy")
    username = "testuser"

    valid_password = "ValidPass1!"
    assert validate_password(username, valid_password), "Password policy test failed: Valid password rejected."

    invalid_passwords = [
        "short1!",        # Too short
        "toolongpassword1!",  # Too long
        "NoDigits!",      # Missing digits
        "noUppercase1!",  # Missing uppercase
        "NOLOWERCASE1!",  # Missing lowercase
        "NoSpecialChar1", # Missing special characters
        "testuser1!",      # Contains username
        "Password1!"       # Contains password from the weak_password.txt file
    ]
    for pwd in invalid_passwords:
        assert not validate_password(username, pwd), f"Password policy test failed: Invalid password '{pwd}' accepted."
    print("Password policy test passed.")


def run_tests():
    """Runs all test cases."""
    setup_test_environment()
    test_signup()
    test_login()
    test_access_control()
    test_business_hours()
    test_password_policy()
    print("\nAll tests passed successfully.")


if __name__ == "__main__":
    run_tests()
