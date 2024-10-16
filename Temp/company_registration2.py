from flask import Flask, request, render_template
import webbrowser
import threading

company_registration2 = Flask(__name__)

@company_registration2.route('/')
def form():
    return render_template('company_registration2.html')  # Ensure form2.html is in the 'templates' folder

@company_registration2.route('/submit', methods=['POST'])
def submit():
    # Retrieve data from the form
    gross_expense = request.form.get('gross_expense')  # Gross expense per year
    gross_income = request.form.get('gross_income')    # Gross income per year
    
    # Check if data is received and print it
    if gross_expense and gross_income:
        print(f'Gross Expense: {gross_expense}, Gross Income: {gross_income}')
        return f'Data received: Gross Expense: {gross_expense}, Gross Income: {gross_income}'
    if not gross_expense or not gross_income:
      return "Missing data. Please fill all fields.", 400


def open_browser():
    # Wait a moment to ensure the server is up, then open the browser
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Use threading to open the browser in a new thread
    threading.Timer(1, open_browser).start()  # Delay set to 1 second
    company_registration2.run(debug=True)
