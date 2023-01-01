from flask import Flask, request, redirect, render_template, url_for, session
from functions import *
from datetime import datetime
app = Flask(__name__)
con = mysql.connector.connect(
    user='root',
    password='toor',
    port='3306',
    host='localhost',
    database='shoe')

cursor = con.cursor()

app.config['SECRET_KEY'] = "lkasfjdlkjlasjfhlkajhfkljash"


@app.route('/edit_inventory', methods=['GET', 'POST'])
def edit_inventory():
    if request.method == 'GET':
        return render_template('edit_inventory.html')
    if request.method == 'POST':
        # handle form submission for editing inventory
        item_name = request.form['item_name']
        new_quantity = request.form['new_quantity']
        # ...

        # Update the inventory in the database
        sql = "UPDATE inventory SET quantity = %s WHERE item_name = %s"
        values = (new_quantity, item_name)
        cursor.execute(sql, values)
        con.commit()

        return 'Inventory edited successfully'
    else:
        # render form for editing inventory
        return render_template('edit_inventory.html')


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'GET':
        return render_template('add_supplier.html')
    if request.method == 'POST':
        # handle form submission for adding supplier
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        contact1 = request.form['contact_1']
        contact2 = request.form['contact_2']
        email = request.form['email']
        supplier_id = generate_supplier_id()
        sql = "INSERT INTO supplier (supplier_id,first_name,last_name, address, contact_1,contact_2,email) VALUES (%s, %s, %s, %s,%s,%s,%s)"
        values = (supplier_id, first_name, last_name,
                  address, contact1, contact2, email)
        cursor.execute(sql, values)
        con.commit()
        msg = "Supplier added successfully"
        return render_template('add_supplier.html', message=msg, category='success')
    else:
        msg = "Supplier already exists"
        return render_template('add_supplier.html', message=msg, category='error')


@app.route('/remove_supplier', methods=['GET', 'POST'])
def remove_supplier():
    if request.method == 'GET':
        return render_template('remove_supplier.html')
    if request.method == 'POST':
        # handle form submission for removing supplier
        supplier_id = request.form['supplier_id']

        if (check_supplierid(supplier_id) == True):
            query = "DELETE FROM supplier WHERE supplier_id = %s"
            values = (supplier_id,)
            cursor.execute(query, values)
            con.commit()
            msg = "Supplier removed successfully"
            return render_template('remove_supplier.html', message=msg, category='success')
        else:
            msg = "Supplier does not exist"
            return render_template('remove_supplier.html', message=msg, category='error')


@app.route('/remove_staff', methods=['GET', 'POST'])
def remove_staff():
    if request.method == 'GET':
        return render_template('remove_staff.html')
    if request.method == 'POST':
        # handle form submission for removing staff member
        staff_id = request.form['staff_id']
        # ...
        # Remove staff member from the database
        if (check_staffid(staff_id) == True):
            query = "DELETE FROM staff WHERE staff_id = %s"
            values = (staff_id,)
            cursor.execute(query, values)
            con.commit()
            query = "DELETE FROM login WHERE staff_id = %s"
            values = (staff_id,)
            cursor.execute(query, values)
            con.commit()
            msg = "Staff member removed successfully"
            return render_template('remove_staff.html', message=msg, category='success')
        else:
            # render form for removing staff member
            msg = "Staff member does not exist"
            return render_template('remove_staff.html', message=msg, category='error')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'role' in session:
            if session['role'] == ('admin'):
                return redirect(url_for('admin_panel'))
            if session['role'] == ('worker'):
                return redirect(url_for('worker_panel'))
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    # Execute a SQL query to check if the username and password match a record in the database
        query = 'SELECT * FROM login WHERE username=%s AND password=%s'
        cursor.execute(query, (username, password))
        # Fetch the results
        result = cursor.fetchone()
        # Return the result
        if result:
            query = f"SELECT role FROM staff WHERE staff_id = '{result[2]}'"
            cursor.execute(query)
            # Fetch the results
            role = cursor.fetchone()
            session['role'] = role
            if (role[0] == 'admin'):
                return redirect(url_for('admin_panel'))
            if (role[0] == 'worker'):
                return redirect(url_for('worker_panel'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)


@app.route('/show_sales', methods=['GET'])
def show_sales():
    # Retrieve daily sales data from the database
    sql = "SELECT * FROM sales"
    cursor.execute(sql)
    sales_data = cursor.fetchall()

    # Display daily sales data
    return render_template('show_sales.html', sales=sales_data)


@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'GET':
        return render_template('register_staff.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        email = request.form['email']
        contact1 = request.form['contact_1']
        contact2 = request.form['contact_2']
        if (check_form_fields(request.form)):
            if is_valid_email(email) == False:
                return render_template('register_staff.html', message="Invalid email", category="error")
            if password != confirm_password:
                error = "Passwords do not match"
                return render_template('register_staff.html', message=error, category="error")
            if check_username(username) == False:
                error = "Username already exists"
                return render_template('register_staff.html', message=error, category="error")
            staff_id = generate_staff_id()
            query = f'INSERT INTO staff (first_name, last_name, role, address, email, contact_1, contact_2, staff_id) VALUES ("{first_name}", "{last_name}", "{role}", "{address}","{email}", "{contact1}", "{contact2}","{staff_id}")'
            cursor.execute(query)
            con.commit()
            query = f'INSERT INTO login (username, password, staff_id) VALUES ("{username}", "{password}", "{staff_id}")'
            cursor.execute(query)
            con.commit()
            msg = "Staff member registered successfully"
            return render_template('register_staff.html', message=msg, category="success")
        else:
            error = "Please fill all the fields"
            return render_template('register_staff.html', message=error, category="error")

    else:
        return render_template('login.html')


@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'GET':
        render_template('register_customer.html')
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_1 = request.form['contact_1']
        contact_2 = request.form['contact_2']
        address = request.form['address']
        email = request.form['email']

        # Generate a random 5-digit customer ID
        customer_id = generate_customer_id()

        # Check if the customer ID already exists in the database
        query = 'SELECT * FROM customer WHERE customer_id = %s'
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()

        # If the customer ID already exists, generate a new one and check again
        while result is not None:
            customer_id = generate_customer_id()
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()

        # Insert the data into the database
        query = 'INSERT INTO customer (customer_id, first_name, last_name, contact_1, contact_2, address, email) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (customer_id, first_name,
                       last_name, contact_1, contact_2, address, email))

        # Commit the changes
        con.commit()

        msg = "Customer member registered successfully"
        return render_template('register_customer.html', message=msg, category="success")
    else:
        # Render the form template
        return render_template('register_customer.html')


@app.route('/search_supplier', methods=['GET', 'POST'])
def search_supplier():
    if request.method == 'GET':
        return render_template('search_supplier.html')
    if request.method == 'POST':
        # Get the search criteria from the form
        search_type = request.form['search_type']
        search_term = request.form['search_term']

        # Construct the SELECT query
        if search_type == 'id':
            query = f"SELECT * FROM supplier WHERE supplier_id = {search_term}"
        elif search_type == 'name':
            query = f"SELECT * FROM supplier WHERE first_name = '{search_term}' OR last_name = '{search_term}'"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Check if there are any results
        if not results:
            msg = "No results found"
            return render_template('search_supplier.html', message=msg, category="error")
        else:
            return render_template('search_supplier.html', results=results)


@app.route('/search_staff', methods=['GET', 'POST'])
def search_staff():
    if request.method == 'GET':
        return render_template('search_staff.html')
    if request.method == 'POST':
        # Get the search criteria from the form
        search_type = request.form['search_type']
        search_term = request.form['search_term']

        # Construct the SELECT query
        if search_type == 'id':
            query = f"SELECT * FROM staff WHERE staff_id = {search_term}"
        elif search_type == 'name':
            query = f"SELECT * FROM staff WHERE first_name = '{search_term}' OR last_name = '{search_term}'"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Check if there are any results
        if not results:
            msg = "No results found"
            return render_template('search_staff.html', message=msg, category="error")
        else:
            return render_template('search_staff.html', results=results)


@app.route('/add_monthly_expenses', methods=['GET', 'POST'])
def add_monthly_expenses():
    if request.method == 'GET':
        return render_template('add_monthly_expenses.html')
    if request.method == 'POST':
        # Read the form data
        electric_bill = request.form['electricity_bill']
        internet_bill = request.form['internet_bill']
        restocking_cost = request.form['restocking_cost']
        rent = request.form['rent']
        date = str(request.form['date']) + '-01'

        # Insert the data into the MySQL database

        cursor = con.cursor()
        sql = f"SELECT * FROM expense WHERE date_by_month = '{date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            # An entry already exists, return a message to the user
            msg = "This month's expenses have already been added"
            return render_template('add_monthly_expenses.html', message=msg, category="error")
        else:
            # Insert the data into the database
            # calculate the sum of all the salaries of staff from the employee table
            cursor = con.cursor()
            sql = f"SELECT SUM(salary) FROM staff"
            cursor.execute(sql)
            result = cursor.fetchone()
            staff_salary = result[0]
            print(staff_salary)
            print(date)
            sql = f"INSERT INTO expense (staff_salary, electric_bill, internet_bill, restocking_cost, rent, date_by_month) VALUES ({staff_salary},{electric_bill}, {internet_bill}, {restocking_cost},{rent}, '{date}')"
            cursor.execute(sql)
            con.commit()
            msg = "Expenses added successfully for the month"
            return render_template('add_monthly_expenses.html', message=msg, category="success")
    else:
        # Render the "Add Monthly Expenses" template
        return render_template('add_monthly_expenses.html')


@app.route('/add_monthly_investments', methods=['GET', 'POST'])
def add_monthly_investments():
    if request.method == 'GET':
        return render_template('add_monthly_investments.html')
    if request.method == 'POST':
        # Read the form data
        investments = request.form['investments']

        date = str(request.form['date']) + '-01'

        # Insert the data into the MySQL database

        cursor = con.cursor()
        sql = f"SELECT * FROM income WHERE date_by_month = '{date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            # An entry already exists, return a message to the user
            msg = "This month's investments have already been added"
            return render_template('add_monthly_investments.html', message=msg, category="error")
        else:
            # Insert the data into the database

            cursor = con.cursor()

            sql = f"INSERT INTO income (investments, date_by_month) VALUES ({investments}, '{date}')"
            cursor.execute(sql)
            con.commit()
            msg = "Investments added successfully for the month"
            return render_template('add_monthly_investments.html', message=msg, category="success")
    else:
        # Render the "Add Monthly Expenses" template
        return render_template('add_monthly_investments.html')


@app.route('/assign_salaries', methods=['GET', 'POST'])
def assign_salaries():
  # Get form data
    if request.method == 'GET':
        return render_template('assign_salaries.html')
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        salary = request.form['salary']
        action = request.form['action']
    # Check if staff member with provided ID exists in the database
        cursor.execute(f"SELECT * FROM staff WHERE staff_id= {staff_id}")
        result = cursor.fetchone()
        if result is None:
            msg = "Staff member does not exist"
            return render_template('assign_salaries.html', message=msg, category="error")

    # Check if salary is a valid number
        try:
            salary = float(salary)
        except ValueError:
            msg = "Invalid Salary"
            return render_template('assign_salaries.html', message=msg, category="error")

    # Perform action based on dropdown selection
        if action == "assign":
            # Insert new row into the staff table
            cursor.execute(
                f"UPDATE staff SET salary={salary} WHERE staff_id={staff_id}")
            con.commit()
            msg = "Salary assigned successfully"
            return render_template('assign_salaries.html', message=msg, category="success")
        elif action == "update":
            # Update salary of staff member in the staff table
            cursor.execute(
                f"UPDATE staff SET salary={salary} WHERE staff_id={staff_id}")
            con.commit()
            msg = "Salary updated successfully"
            return render_template('assign_salaries.html', message=msg, category="success")


@app.route('/view_staff', methods=['GET'])
def view_staff():
    # Execute a SELECT query to retrieve all rows from the staff table
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM staff')
        results = cursor.fetchall()

    # Render the staff template, passing in the rows from the query as a variable
    return render_template('view_staff.html', results=results)


@app.route('/add_items', methods=['GET', 'POST'])
def add_items():
    if request.method == 'GET':
        return render_template('add_items.html')
    if request.method == 'POST':
        # Get the form data
        item_name = request.form['item_name']
        itype = request.form['type']
        brand = request.form['brand']
        quantity = request.form['quantity']
        price = request.form['price']
        supplier = request.form['supplier_id']
        # Generate a random 5-digit item ID
        import random
        item_id = random.randint(10000, 99999)

        # Insert the item into the database
        cursor = con.cursor()
        query = "INSERT INTO item (item_id, item_name, type, brand, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (item_id, item_name,
                       itype, brand, quantity, price))
        con.commit()
        cursor.execute(
            f"SELECT * FROM supplier_item WHERE item_id= {item_id} and supplier_id = {supplier}")
        result = cursor.fetchone()
        if result is None:
            query = "INSERT INTO supplier_item (item_id, supplier_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (item_id, supplier,
                                   quantity))
            con.commit()
        else:
            query = f"SELECT quantity from supplier_item WHERE item_id= {item_id} and supplier_id = {supplier}"
            cursor.execute(query, (item_id, supplier,
                                   quantity))
            result = cursor.fetchone()
            result += int(quantity)
            query = f"UPDATE supplier.item SET quantity = {result} WHERE supplie_id={supplier} and item_id = {item_id}"
            cursor.execute(query)
            con.commit()
        msg = "Items added successfully"
        return render_template('add_items.html', message=msg, category="success")
    else:
        # Render the "Add Items" form
        msg = "Item could not be added successfully"
        return render_template('add_items.html', message=msg, category="error")


@app.route("/financial_analysis", methods=['GET', 'POST'])
def financial_analysis():
    if request.method == 'GET':
        return render_template('financial_analysis.html')
    if request.method == 'POST':
        date = str(request.form['date']) + '-01'
        query = f"Select income.date_by_month,income.total_income AS Total_income,expense.total_expense AS Total_expense,income.total_income - expense.total_expense as net_income FROM expense JOIN Income on income.date_by_month=expense.date_by_month where income.date_by_month=DATE_ADD('{date}', INTERVAL 1 MONTH);"
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        if results is None:
            msg = "No data found"
            return render_template('financial_analysis.html', message=msg, category="error")
        else:
            return render_template('financial_analysis.html', results=results)


@app.route('/delete_items', methods=['GET', 'POST'])
def delete_items():
    if request.method == "GET":
        return render_template('delete_items.html')
    if request.method == "POST":
        item_id = request.form['item_id']
        # Check if the item exists by retrieving it from the database
        sql = "SELECT * FROM item WHERE item_id = %s"
        values = (item_id,)
        cursor.execute(sql, values)
        item = cursor.fetchone()

        if not item:
            msg = 'No item found'
            return render_template('delete_items.html', msg=msg, category="success")
        # Use the item ID to create a DELETE SQL statement
        sql = "DELETE FROM item WHERE item_id = %s"
        values = (item_id,)
        # Execute the DELETE statement
        cursor.execute(sql, values)
        con.commit()
        msg = 'Item successfully deleted'
        return render_template('delete_items.html', msg=msg, category="success")


@app.route('/punch_invoice', methods=['GET', 'POST'])
def punch_invoice():
    if request.method == 'GET':
        return render_template('punch_invoice.html')
    if request.method == 'POST':
        price = request.form['price']
        pID = request.form['shoe_id']
        quantity = request.form['quantity']
        cID = request.form['customer_id']
        discount = request.form['price']
        time = str(datetime.now())[:19]
        inv_id = generate_invoice_id()

        # Getting the username of the employee ?????
        Emp_id = "26663"  # hard coded for now

        if check_productID(pID) == True and check_customerID(cID) == True:
            query = f'INSERT INTO invoice (invoice_id, bill, date_time, customer_id, staff_id) VALUES ("{inv_id}", "{price}", "{time}", "{cID}", "{Emp_id}")'
            cursor.execute(query)
            con.commit()
            query = f'INSERT INTO invoice_item (invoice_id, item_id, quantity, discount) VALUES ("{inv_id}", "{pID}", "{quantity}", "{discount}")'
            cursor.execute(query)
            con.commit()
        elif check_productID(pID) == False:
            err = "Product does not exist!"
            return render_template('punch_invoice.html', error=err)
        elif check_customerID(cID) == False:
            err = "This customer does not exist in the database!"
            return render_template('punch_invoice.html', error=err)

        return render_template('punch_invoice.html', category="success")


@app.route('/search_a_shoe.html', methods=['GET', 'POST'])
def search_a_shoe():
    if request.method == 'GET':
        return render_template("search_a_shoe.html")
    if request.method == 'POST':
        cat = request.form['category']
        search_by = request.form['name']
        query = f'select * from item where {cat} = {search_by}'
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("search_a_shoe.html", headings=("item_id", "item_name", "type", "brand", "quantity", "price"), data=data)


@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/home')
def home():
    return render_template('login1.html')


if __name__ == '__main__':
    app.run()
