# Problem 2: Password Management
from hashlib import blake2b
import secrets
import os

FILENAME = "passwd.txt"
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE_PATH = os.path.join(SCRIPT_PATH, FILENAME)

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
