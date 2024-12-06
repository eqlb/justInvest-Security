# **justInvest User Authentication and Access Control System**

This assignment implements a prototype user authentication and access control system for justInvest. It supports role-based access control (RBAC), proactive password validation, and restricted access for specific roles (e.g., Tellers) based on business hours.

---

## **Features**

1. **User Signup**:
   - Securely stores usernames, hashed passwords (BLAKE2b), salts, and roles.
   - Enforces a proactive password policy:
     - Passwords must be 8-12 characters long.
     - Must include uppercase, lowercase, digits, and special characters (`!@#$%^&*`).
     - Must not include the username.
     - Must not match common weak passwords.
   - Validates roles during registration.

2. **User Login**:
   - Authenticates users by verifying their password against stored credentials.
   - Displays role-based access rights after successful login.

3. **Access Control**:
   - Uses RBAC to allow or deny operations based on user roles.
   - Roles and permissions:
     - **Client**: View account balance, view portfolio, contact Financial Advisor.
     - **Premium Client**: Includes all Client privileges + modify portfolio, contact Financial Planner.
     - **Financial Advisor**: Includes all Client privileges + modify portfolio, view private consumer instruments.
     - **Financial Planner**: Includes all Client privileges + view money market instruments, view private consumer instruments.
     - **Teller**: Restricted to viewing account balance and portfolio during business hours (9 AM - 5 PM).

4. **Business Hours Restriction**:
   - Tellers can only access the system during defined business hours.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/eqlb/justInvest-security.git
   cd justInvest-security
   
2. **Setup Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Run the program**:

# **justInvest User Authentication and Access Control System**

## **Usage**

### **1. Register a New User**
- Enter a unique username.
- Select a role from the list: Client, Premium Client, Financial Advisor, Financial Planner, Teller.
- Create a password that adheres to the password policy.

### **2. Login**
- Enter your registered username and password.
- On successful login, your role and allowed operations will be displayed.

### **3. Perform Operations**
- Enter the number corresponding to the desired operation.
- Unauthorized operations will result in an "Access Denied!" message.

### **4. Teller Restrictions**
- Tellers can only log in and access the system between 9 AM and 5 PM.
- Attempting access outside this window will result in a denial message.

---

## **Password Policy**
The system enforces the following rules for passwords:
1. **Must be 8-12 characters long.**
2. **Must include:**
   - At least one uppercase letter.
   - At least one lowercase letter.
   - At least one digit.
   - At least one special character (`!@#$%^&*`).
3. **Must not include the username.**
4. **Must not match any password in the weak passwords list (e.g., `password`, `123456`).

---

## **Project Structure**

justInvest-security/
├── assignment.py        # All code combined
├── Problem1.py        # Problem 1
├── Problem2.py        # Problem 2
├── Problem3.py        # Problem 3
├── Problem4.py        # Problem 4
├── passwd.txt           # Password file (auto-generated during runtime)
├── test.py              # Test script
├── README.md            # Documentation

## **Testing**

### **Run the test suite to validate all functionality:**
## Tests Include:
1. Signup: Verifies user registration.
2. Login: Tests authentication and role-based access control.
3. Access Control: Ensures operations are correctly allowed or denied.
4. Business Hours: Validates Teller restrictions.
5. Password Policy: Tests adherence to password rules.



