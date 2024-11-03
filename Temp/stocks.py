from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import threading
import webbrowser

stocks = Flask(__name__)
stocks.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vivek@123',
    'database': 'project'
}

# Function to check login credentials and fetch profile data without passwords
def check_login(username, passwords):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Select only username, email, and phone (exclude passwords)
        query = "SELECT username, email, phone FROM users WHERE username = %s AND passwords = %s"
        cursor.execute(query, (username, passwords))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print("Database error during login:", err)
        return None

# Function to register a user or company with a password
def register_user(username, email, phone, passwords, user_type):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, email, phone, passwords, user_type) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, email, phone, passwords, user_type))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print("Database error during registration:", err)
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
        username = request.form['username']
        passwords = request.form['passwords']
        user_data = check_login(username, passwords)
        if user_data:
            return render_template('user_information.html', user=user_data)
        else:
            return "<h2>Wrong username or password entered</h2>"
    return render_template('user_login.html')

@stocks.route('/company/login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        username = request.form['username']
        passwords = request.form['passwords']
        company_data = check_login(username, passwords)
        if company_data:
            return render_template('company_information.html', company=company_data)
        else:
            return "<h2>Wrong username or password entered</h2>"
    return render_template('company_login.html')

@stocks.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        passwords = request.form['passwords']
        if register_user(username, email, phone, passwords, 'user'):
            return "<h2>Registration Successful</h2>"
        else:
            return "<h2>Registration Failed</h2>"
    return render_template('user_register.html')

@stocks.route('/company/register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        passwords = request.form['passwords']
        if register_user(username, email, phone, passwords, 'company'):
            return "<h2>Registration Successful</h2>"
        else:
            return "<h2>Registration Failed</h2>"
    return render_template('company_register.html')

# Function to automatically open the browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

# Start the Flask server and open the browser automatically
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    stocks.run(debug=True)
#3