from user import register, login, admin_login, add_scooter, rent_scooter, stop_scooter, logout


# Function to display user menu
def user_menu():
    txt = """
    1. Rent a scooter through ID
    2. Stop scooter
    """
    print(txt)
    user_input = int(input("Choose from menu: "))
    if user_input == 1:
        if rent_scooter():
            show_menu()  # After renting, show main menu again
        else:
            print("Scooter not available. Please try again.")
            user_menu()  # If scooter is not available, prompt user to try again
    elif user_input == 2:
        if stop_scooter():
            show_menu()  # After stopping scooter, show main menu again
        else:
            print("Scooter not available. Please try again.")
            user_menu()  # If scooter is not available to stop, prompt user to try again


# Function to display main menu
def show_menu():
    txt = """
    1. Register user
    2. Admin login to add scooter
    3. User menu
    4. Exit
    """
    print(txt)
    user_input = int(input("Choose from menu: "))
    if user_input == 1:
        if register():
            show_menu()  # After successful registration, show main menu again
        else:
            print("Registration failed. Please try again.")
            show_menu()  # If registration fails, prompt user to try again
    elif user_input == 2:
        if admin_login():
            add_scooter()  # If admin login successful, proceed to add scooter
        show_menu()  # Show main menu again regardless of admin login success or failure

    elif user_input == 3:
        if login():
            user_menu()  # If user login successful, show user menu
        else:
            print("Invalid credentials. Please try again.")
            show_menu()  # If login fails, prompt user to try again
    elif user_input == 4:
        logout()  # Logout and exit program
    else:
        print("Invalid choice. Please try again.")
        show_menu()  # If user enters invalid menu option, prompt user to try again


# Entry point of the program
if __name__ == "__main__":
    show_menu()
