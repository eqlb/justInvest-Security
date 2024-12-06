# Problem 1: Access Control Mechanism
ACCESS_CONTROL_POLICY = {
    "Client": [1, 2, 4],
    "Premium Client": [1, 2, 3, 4, 5],
    "Financial Advisor": [1, 2, 3, 7],
    "Financial Planner": [1, 2, 3, 6, 7],
    "Teller": [1, 2]
}

BUSINESS_DAY_START_HOUR = 9
BUSINESS_DAY_CLOSE_HOUR = 17

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
