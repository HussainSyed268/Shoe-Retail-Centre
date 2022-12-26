import re
import random
from flask import render_template
import mysql.connector

con = mysql.connector.connect(
    user='root',
    password='toor',
    port='3306',
    host='localhost',
    database='shoe')

cursor = con.cursor()


def check_form_fields(form_data):
    # Initialize a flag to keep track of whether all fields are filled
    all_fields_filled = True

    # Check if the address field is empty
    if not form_data['address']:
        all_fields_filled = False
        return render_template('signup.html', error="Please enter the address.")

    # Check if the contact1 field is empty
    if not form_data['contact_1']:
        all_fields_filled = False
        return render_template('signup.html', error="Please enter the contact number.")

    # Check if the role field is empty
    if not form_data['role']:
        all_fields_filled = False
        return render_template('signup.html', error="Please select the role.")

    # Check if the username field is empty
    if not form_data['username']:
        all_fields_filled = False
        return render_template('signup.html', error="Please enter the username.")

    # Check if the password field is empty
    if not form_data['password']:
        all_fields_filled = False
        return render_template('signup.html', error="Please enter the password.")
    # Return the flag indicating whether all fields are filled
    return all_fields_filled


def generate_staff_id():
    # Generate a random 5-digit staff ID
    staff_id = random.randint(10000, 99999)
    # Check if the staff ID exists in the database
    query = "SELECT * FROM staff WHERE staff_id = %s"
    cursor.execute(query, (staff_id,))
    result = cursor.fetchone()

    # If the staff ID exists in the database, generate a new one
    while result:
        staff_id = random.randint(10000, 99999)
        cursor.execute(query, (staff_id,))
        result = cursor.fetchone()
    # Return the staff ID
    return staff_id


def is_valid_email(email):
    # Define the pattern for a valid email address
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    # Use the search function to search for the pattern in the email string
    result = re.search(pattern, email)
    # If the search function returns a match, the email is valid
    if result:
        return True
    # If the search function returns None, the email is invalid
    else:
        return False


def check_username(username):
    # Check if the username exists in the database
    query = "SELECT * FROM login WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # If the staff ID exists in the database, generate a new one
    if result:
        return False
    # Return the staff ID
    else:
        return True


def check_staffid(id):
    query = "SELECT * FROM login WHERE staff_id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    if result:
        return True
    # Return the staff ID
    else:
        return False


def check_supplierid(id):
    query = "SELECT * FROM supplier WHERE supplier_id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    if result:
        return True
    # Return the staff ID
    else:
        return False


def generate_supplier_id():
    # Generate a random 5-digit staff ID
    supplier_id = random.randint(1000, 9999)
    # Check if the staff ID exists in the database
    query = "SELECT * FROM supplier WHERE supplier_id = %s"
    cursor.execute(query, (supplier_id,))
    result = cursor.fetchone()

    while result:
        supplier_id = random.randint(1000, 9999)
        cursor.execute(query, (supplier_id,))
        result = cursor.fetchone()

    return supplier_id
