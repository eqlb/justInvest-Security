# Problem 4: Login and User Interaction
from Problem1 import*
from Problem2 import*
from Problem3 import*

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


def user_selection():
    """Handles user operation selection."""
    while True:
        try:
            return int(input("Which operation would you like to perform? Enter 0 to quit.\n"))
        except ValueError:
            print("Invalid input. Please enter a number.")


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