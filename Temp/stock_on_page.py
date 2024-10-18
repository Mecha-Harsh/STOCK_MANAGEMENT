from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configure your MySQL connection
db_config = {
    'user': 'root',
    'password': 'harsh@125',
    'host': 'localhost',
    'database': 'stock_exp'
}

# Function to fetch stock prices from the database
def fetch_stock_prices():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
    
    # Fetch column names (stock names) and row data (prices)
    columns = cursor.column_names[1:]  # Skip timestamp column
    row = cursor.fetchone()[1:]  # Skip timestamp value
    
    cursor.close()
    connection.close()
    return columns, row

@app.route('/')
def index():
    columns, prices = fetch_stock_prices()
    return render_template('index1.html', stocks=zip(columns, prices))

if __name__ == '__main__':
    app.run(debug=True)
