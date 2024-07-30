import os
import json

Admin_login = 'admin'
Admin_password = '0000'


class JsonManager:
    def __init__(self, filename):
        self.file_name = filename

    def check_file_exists(self):
        return os.path.exists(self.file_name)

    def read_json_file(self):
        if self.check_file_exists():
            if os.path.getsize(self.file_name) != 0:
                with open(self.file_name, "r") as file:
                    return json.load(file)
            return []  # Return empty list if file exists but empty
        return []  # Return empty list if file does not exist

    def write_json_file(self, data):
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)
            return "Data added successfully"

    # Add new data to the JSON file
    def add_to_file(self, data):
        items = self.read_json_file()  # Read existing data
        items.append(data)  # Append new data
        self.write_json_file(items)  # Write updated data to file
        return "Data added successfully"  # Confirmation message


# Instances of JsonManager for managing different JSON files
scooter_manager = JsonManager('./data/scooters.json')
user_manager = JsonManager('./data/users.json')
rental_manager = JsonManager('./data/rentals.json')
