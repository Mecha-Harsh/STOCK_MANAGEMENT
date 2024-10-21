from flask import Flask, render_template, request, redirect
import subprocess

app = Flask(__name__)
subprocess.Popen(['python', 'main_table.py'])
# Route for the login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route for handling login submission
@app.route('/login', methods=['POST'])
def login():
    # Start the main_table.py application
    process5=subprocess.Popen(['python','Temp\main_table.py'])
  # Use parentheses for Popen
    username = request.form.get('username')  # Get the username from the form
    print(f"Username: {username}")  # Print the username to the terminal
    # Redirect to the main_table app running on a different port
    return redirect("http://127.0.0.1:5000/")  # Adjust based on your main_table.py app

if __name__ == '__main__':
    app.run(debug=True,port=5001)
