from flask import Flask, redirect, request, render_template, url_for
import webbrowser
from createdatabase import set_database
import threading
import subprocess


cursor, con = set_database()
compid = []  # Initialize the compid variable globally
app = Flask(__name__)

# Route for the first form
@app.route('/')
def form():
    return render_template('company_registration_1.html')  # Ensure this file is in the 'templates' folder

# Route to handle submission of the first form
@app.route('/submit', methods=['POST'])
def submit():
    global compid  # Declare global compid to modify it
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')

    sql_value = f"INSERT INTO company_detail (comp_name, email, phone_no, address) VALUES ('{name}', '{email}', '{phone}', '{address}')"
    get_compid = f"SELECT comp_id FROM company_detail WHERE comp_name='{name}' AND email='{email}'"
    
    if cursor:
        try:
            cursor.execute(sql_value)
            con.commit()
            
            cursor.execute(get_compid)
            compid = cursor.fetchall()
            compid=compid[0]
            if compid:
                print(f"Company ID fetched: {compid[0]}")
            else:
                print("No company ID found for the given details.")
            
        except Exception as e:
            print(f"Error executing query: {e}")
            return "Internal Server Error", 500
    else:
        print("No connection found")
        return "Database Connection Error", 500
        
    return redirect(url_for('form2'))  # Redirect to the second form

# Route for the second form
@app.route('/form2')
def form2():
    return render_template('company_registration2.html')  # Ensure this file is in the 'templates' folder

# Route to handle submission of the second form
@app.route('/submit_form2', methods=['POST'])
def submit_form2():
    global compid
    gross_expense = request.form.get('gross_expense')
    gross_income = request.form.get('gross_income')
    print(gross_expense, gross_income)
    if cursor and compid:
        price = int((float(gross_income) - float(gross_expense)) / 5)
        # Use parameterized query
        data_entry = "INSERT INTO stock_initial (comp_id, stock_id ,gross_expense, gross_income, stock_price) VALUES (%s, %s, %s, %s,%s)"
        
        try:
            cursor.execute(data_entry, (compid[0],compid[0], gross_expense, gross_income, price))
            con.commit()
            print("Stock information inserted successfully.")
        except Exception as e:
            print(f"Error inserting stock data: {e}")
            return "Internal Server Error", 500
    str=r"main\addingstocktostock_prices.py"
    process2 = subprocess.Popen(['python', str])
    process2.wait()
    return redirect(url_for('thank_you'))

# Route for the thank you page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')  # Ensure this file is in the 'templates' folder

# Function to open the web browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()  # Delay set to 1 second
    app.run(debug=True)  # Enable debug mode
