import hashlib
from json_manager import Admin_login, Admin_password, user_manager, scooter_manager, rental_manager
import random
from datetime import datetime


# Class representing a User with username, password, and login status
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_login = False

    # Static method to hash a password using SHA-256
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()


# Function to register a new user
def register():
    try:
        username = input("Enter your username: ").capitalize().strip()
        password = hashlib.sha256(input('Password: ').strip().encode()).hexdigest()
        confirm_password = hashlib.sha256(input("Confirm your password: ").strip().encode()).hexdigest()
        if password != confirm_password:
            print("Passwords do not match.")
            return False
        user = User(username, password)
        user_manager.add_to_file(user.__dict__)
        print("Registration successful.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Function to log in a user
def login():
    try:
        username = input("Enter your username: ").capitalize().strip()
        password = input("Enter your password: ")
        hash_password = User.hash_password(password)
        data = user_manager.read_json_file()
        for user in data:
            if user["username"] == username and user["password"] == hash_password:
                print("Login successful.")
                user["is_login"] = True
                user_manager.write_json_file(data)
                return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Function to log out a user
def logout():
    data = user_manager.read_json_file()
    for user in data:
        if user["is_login"]:
            user["is_login"] = False
        user_manager.write_json_file(data)
    print("Goodbye!")


# Function to retrieve scooter information from data
def get_scooter(data):
    for scooter in data:
        if scooter["scooter_id"]:
            print(
                f"Scooter ID:{scooter['scooter_id']},\nModel: {scooter['model']},\n"
                f"Price per min: {scooter['price_per_min']}\n")


# Function to rent a scooter
def rent_scooter():
    try:
        data = scooter_manager.read_json_file()
        get_scooter(data)
        scooter_id = int(input("Enter scooter ID: "))
        for scooter in data:
            if scooter["scooter_id"] == scooter_id:
                if scooter["is_rented"]:
                    print("This scooter is currently being used by another user.")
                    return False
                else:
                    print("Scooter rented successfully.")
                    rent_data = {
                        "scooter_id": scooter_id,
                        "start_time": str(datetime.now()),
                        "work_time": None,
                        "total_price": None
                    }
                    scooter["is_rented"] = True
                    scooter_manager.write_json_file(data)
                    rental_manager.add_to_file(rent_data)
                    print(f"Scooter {scooter['model']} rented successfully!")
                    return True
        print("Scooter not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def stop_scooter():
    try:
        scooter_id = int(input("Enter scooter ID to stop: "))
        data_scooters = scooter_manager.read_json_file()
        if data_scooters:
            for price in data_scooters:
                data = rental_manager.read_json_file()
                for scooter in data:
                    if scooter["scooter_id"] == scooter_id and scooter['work_time'] is None:
                        scooter['work_time'] = datetime.now().isoformat()
                    start_time = datetime.strptime(scooter['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                    work_time = datetime.now() - start_time
                    duration_minutes = work_time.total_seconds() / 60
                    total_price = duration_minutes * price['price_per_min']
                    scooter['total_price'] = total_price
                    rental_manager.write_json_file(data)
                    print(f"Scooter {price['model']} stopped successfully!")
            return True

    except Exception as e:
        print(f"An error occurred: {e}")
    return False


class Scooter:
    def __init__(self, scooter_id, model, charge, location, price_per_min):
        self.scooter_id = scooter_id
        self.model = model
        self.charge = charge
        self.location = location
        self.price_per_min = price_per_min
        self.is_rented = False


def add_scooter():
    try:
        scooter_id = random.randint(1, 999)
        model = input("Enter scooter model: ").capitalize()
        charge = input("Enter scooter charge: ")
        location = input("Enter scooter location: ").capitalize()
        price_per_min = float(input("Enter scooter price min: "))
        scooter = Scooter(scooter_id, model, f"{charge}%", location, price_per_min)
        scooter_manager.add_to_file(scooter.__dict__)
        print("Scooter added successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def admin_login():
    admin_username = input("Enter the admin login (admin): ").lower().strip()
    admin_password = input("Enter the admin password (0000): ")
    if admin_username == Admin_login and admin_password == Admin_password:
        print("Admin login successful.")
        return True
    else:
        print("Invalid admin credentials.")
        return False
