from flask import Flask, request, redirect, render_template, url_for, session
from functions import *
from cryptography.fernet import Fernet
import base64
from datetime import datetime

app = Flask(__name__)
key = Fernet.generate_key()
con = mysql.connector.connect(
    user='root',
    password='toor',
    port='3306',
    host='localhost',
    database='shoe')

cursor = con.cursor()

app.config['SECRET_KEY'] = "lkasfjdlkjlasjfhlkajhfkljash"


# @app.route('/register_staff', methods=['GET', 'POST'])
# def register_staff():
#     if request.method == 'GET':
#         return render_template('register_staff.html')
#     if request.method == 'POST':
#         # handle form submission for registering new staff member
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         # ...

#         # Insert new staff member into the database
#         sql = "INSERT INTO staff (first_name, last_name) VALUES (%s, %s)"
#         values = (first_name, last_name)
#         cursor.execute(sql, values)
#         con.commit()

#         return 'Staff member registered successfully'
#     else:
#         # render form for registering new staff member
#         return render_template('register_staff.html')


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
                return redirect(url_for('admin'))
            if session['role'] == ('cashier'):
                return redirect(url_for('cashier'))
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    # Execute a SQL query to check if the username and password match a record in the database
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
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
                return redirect(url_for('admin'))
            if (role[0] == 'cashier'):
                return redirect(url_for('cashier'))
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
        if check_form_fields(request.form):
            if is_valid_email(email) == False:
                return render_template('register_staff.html', error="Invalid email")
            if password != confirm_password:
                error = "Passwords do not match"
                return render_template('register_staff.html', error=error)
            if check_username(username) == False:
                error = "Username already exists"
                return render_template('register_staff.html', error=error)
            staff_id = generate_staff_id()
            query = f'INSERT INTO staff (first_name, last_name, role, address, email, contact_1, contact_2, staff_id) VALUES ("{first_name}", "{last_name}", "{role}", "{address}","{email}", "{contact1}", "{contact2}","{staff_id}")'
            cursor.execute(query)
            con.commit()
            query = f'INSERT INTO login (username, password, staff_id) VALUES ("{username}", "{password}", "{staff_id}")'
            cursor.execute(query)
            con.commit()
        msg = "Staff member registered successfully"
        return render_template('register_staff.html', message=msg, category="success")


@app.route('/admin')
def admin():
    return render_template('admin_panel.html')


@app.route('/home')
def home():
    return render_template('login1.html')

@app.route('/punch_invoice', methods=['GET', 'POST'])
def punch_invoice():
    if request.method == 'GET':
        return render_template('punch_invoice.html')
    if request.method == 'POST':
        price = request.form['price']
        pID = request.form['product_id']
        cID = request.form['customer_id']
        time = str(datetime.now())[:19]
        inv_id = generate_invoice_id()

        # Getting the username of the employee ?????
        Emp_id = 10 # hard coded for now

        if check_productID(pID) == True and check_customerID(cID) == True:
            query = f'INSERT INTO invoice ("invoice_id", "bill", "date_time", "customer_id", "staff_id") VALUES ("{inv_id}", "{price}", "{time}", "{cID}", "{Emp_id}")'
            cursor.execute(query)
            con.commit()
            query = f'INSERT INTO invoice_item ("invoice_id", "item_id", "quantity", "discount") VALUES ("{inv_id}", "{pID}", "{time}", "{cID}")'
            cursor.execute(query)
            con.commit()
        elif check_productID(pID) == False:
            err = "Product does not exist!"
            return render_template('register_staff.html', error=err)
        elif check_customerID(cID) == False:
            err = "This customer doesnot exist in the database!"
            return render_template('register_staff.html', error=err)
        
        return render_template('register_staff.html', category="success")

@app.route('/search_a_shoe.html')
def search_a_shoe():
    if request.method == 'GET':
        return render_template("search_a_shoe.html")
    if request.method == 'POST':
        cat = request.form['category']
        search_by = request.form['name']
        query = f'select * from item where {cat} = {search_by}'
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("search_a_shoe.html", headings=("item_id", "item_name", "type", "brand", "quantity", "price"), data= data)

if __name__ == '__main__':
    app.run()
