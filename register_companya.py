from flask import Flask, redirect, request, render_template, url_for
import webbrowser
from createdatabase import set_database
import threading

cursor, con = set_database()

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('company_registration_1.html')  # Ensure company_registration_1.html is in the 'templates' folder

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve data from the form
    name = request.form.get('name')  # Use .get() for safety
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    # Check if data is received and print it
    sql_value = f"INSERT INTO company_detail (comp_name, email, phone_no, address) VALUES ('{name}', '{email}', '{phone}', '{address}')"
    print(sql_value)
    
    if cursor:
        cursor.execute(sql_value)
        con.commit()
        print("success!")
    else:
        print("no connection found")
        
    return redirect(url_for('company_registration_2', name=name))  # Redirect to the new route

@app.route('/company_registration_2')
def company_registration_2():
    name = request.args.get('name')
    return f"Thank you, {name}! Your registration is complete."  # Simple thank you page

def open_browser():
    # Wait a moment to ensure the server is up, then open the browser
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Use threading to open the browser in a new thread
    threading.Timer(1, open_browser).start()  # Delay set to 1 second
    app.run()
