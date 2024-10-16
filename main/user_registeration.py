from flask import Flask, request, render_template
import webbrowser
import threading
from createdatabase import set_database

cursor , con = set_database()

app = Flask(__name__)

# Route for the form  
@app.route('/')
def form():
    return render_template('user_registeration.html')  # Make sure 'register.html' is in the 'templates' folder

# Route for handling form submission
@app.route('/submit', methods=['POST'])
def submit():
    firstname = request.form.get('fname')  
    lastname = request.form.get('lname')
    name = f"{firstname} {lastname}"
    email = request.form.get('email')
    password = request.form.get('pswd')
    age = request.form.get('age')
    phonenumber = request.form.get('pnumber')
    gender = request.form.get('gender')

    if cursor:
        enter_data = f"INSERT INTO customer (name, email, phone, password, age, gender) VALUES ('{name}', '{email}', '{phonenumber}', '{password}', {age}, '{gender}');"
        try:
            cursor.execute(enter_data)
            con.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            return "Internal Server Error", 500


def open_browser():
    # Wait a moment to ensure the server is up, then open the browser
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Use threading to open the browser in a new thread
    threading.Timer(1, open_browser).start()  # Delay set to 1 second
    app.run(debug=True)
