from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import webbrowser
import threading
import subprocess
import os
from createdatabase import set_database

# Set up database connection
cursor, conn = set_database()

stocks = Flask(__name__)
stocks.secret_key = 'your_secret_key'  # Set a secret key for session management

def check_login(email, password):
    try:
        query = "SELECT * FROM customer WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print("Database error:", err)
        return False

def register_customer(name, email, phone, password, age, gender):
    try:
        query = "INSERT INTO customer (name, email, phone, password, age, gender) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, password, age, gender))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Database error:", err)
        return False

@stocks.route('/')
def welcome():
    return render_template('welcome.html')

@stocks.route('/user-options')
def user_options():
    return render_template('user_options.html')

@stocks.route('/company-options')
def company_options():
    return render_template('company_options.html')

@stocks.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        if check_login(email, password):
            query = f"select cust_id from customer where email='{email}' and password ='{password}'"
            cursor.execute(query)
            id = cursor.fetchone()
            id = id[0]
            new_app_path = r'main\main_page_customer.py'
            # Start the new application in a new console
            process = subprocess.Popen(['python', new_app_path,str(id)])
            webbrowser.open_new(('http://127.0.0.1:5002/'))
            
            return "<h2>Login Successful</h2>"
        else:
            return "<h2>Wrong email or password entered</h2>"
    return render_template('user_login.html')

@stocks.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        age = request.form.get('age')
        gender = request.form.get('gender')
        if register_customer(name, email, phone, password, age, gender):
            return render_template('success.html', message="Registration Successful")
        else:
            return "<h2>Registration Failed</h2>"
    return render_template('user_register.html')


@stocks.route('/company/register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        passw = request.form['pass']
        sql_value = "INSERT INTO company_detail (comp_name, email, phone_no, address, password) VALUES (%s, %s, %s, %s, %s)"
        get_compid = "SELECT comp_id FROM company_detail WHERE comp_name=%s AND email=%s"

        if cursor:
            try:
                cursor.execute(sql_value, (name, email, phone, address, passw))
                conn.commit()

                cursor.execute(get_compid, (name, email))
                compid = cursor.fetchone()
                if compid:
                    session['compid'] = compid[0]
                    print(f"Company ID fetched: {compid[0]}")
                else:
                    print("No company ID found for the given details.")

            except Exception as e:
                print(f"Error executing query: {e}")
                return "Internal Server Error", 500
        else:
            print("No connection found")
            return "Database Connection Error", 500

        return render_template('success.html', message="Company Registration Successful")

    return render_template('company_registration1.html')


@stocks.route('/company/financial-details', methods=['GET', 'POST'])
def company_registration2():
    return render_template('company_registration2.html')

@stocks.route('/company/submit-financial-details', methods=['POST'])
def submit_form2():
    if request.method == 'POST':
        gross_expense = request.form.get('gross_expense')
        gross_income = request.form.get('gross_income')

        # Validate and convert the inputs
        try:
            gross_expense = int(gross_expense)
            gross_income = int(gross_income)
        except ValueError:
            return "Invalid input for financial details", 400  # Handle invalid input

        price = int((gross_income - gross_expense) / 5)

        # Retrieve the company ID from session
        compid = session.get('compid')  # Get from session
        if compid is None:
            return "Company ID not found", 400  # Handle the error

        # Use parameterized query
        initial_stock = 10000
        data_entry = "INSERT INTO stock_initial (comp_id,initial_stock ,stock_id, gross_expense, gross_income, stock_price) VALUES (%s,%s ,%s, %s, %s, %s)"
        try:
            cursor.execute(data_entry, (compid,initial_stock ,compid, gross_expense, gross_income, price))
            conn.commit()
            print("Stock information inserted successfully.")
        except Exception as e:
            print(f"Error inserting stock data: {e}")
            return "Internal Server Error", 500

        str = r"main\addingstocktostock_prices.py"
        process2 = subprocess.Popen(['python', str])  # Pass port as an argument
        return "<h2>Financial Details Submitted Successfully</h2>"
    
@stocks.route('/company/login', methods=['GET', 'POST'])

@stocks.route('/company/login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check login credentials
        if check_company_login(email, password):
            # Path to the new application
            query_id = f"Select comp_id from company_detail where email='{email}' and password='{password}'"
            cursor.execute(query_id)
            id = cursor.fetchone()
            id = id[0]
            
            new_app_path = r'main\main_page_company.py'
            # Start the new application in a new console
            process = subprocess.Popen(['python', new_app_path,str(id)])
            webbrowser.open_new(('http://127.0.0.1:5001/'))            
            # Return a response to indicate that the new app is starting
            return "<h2>Company Login Successful. The new application is starting.</h2>"
        else:
            return "<h2>Wrong email or password entered</h2>"
    return render_template('company_login.html')


def check_company_login(email, password):
    try:
        query = "SELECT * FROM company_detail WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print("Database error:", err)
        return False


def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    stocks.run(debug=False,port=5000)
