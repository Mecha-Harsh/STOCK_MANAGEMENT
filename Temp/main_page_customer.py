from flask import Flask, render_template, request, make_response
from stock_update_final import get_data
from createdatabase import set_database

# Initialize database connection
cursor, con = set_database()

# Example user id, later to be changed to the one of the user who has logged in
user_id = 1


def get_owned_stock_data():
    user_data = []
    query = f"SELECT stock_id, stock_name, quantity FROM owned_stock WHERE cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        value = {
            "id": row[0],
            "name": row[1],
            "quantity": row[2]
        }
        user_data.append(value)
    return user_data


app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    # Pass random number to prevent iframe caching
    random_num = 42  # You can generate this dynamically as needed
    return render_template('main.html', random_num=random_num)

# Route for the stock table page
@app.route('/stock-table')
def stock_table():
    stocks = get_data()  # Get stock data from the database
    response = make_response(render_template('table.html', stocks=stocks))
    
    # Disable caching for dynamic content
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

# Route for handling stock transactions (buy/sell)
@app.route('/submit-transaction', methods=['POST'])
def submit_transaction():
    stock_id = int(request.form.get('stock_id'))  # Get stock ID from form and convert to integer
    quantity = int(request.form.get('quantity'))   # Get quantity from form and convert to integer
    action = request.form.get('action')             # Get action (buy/sell) from button

    get_quantity = f"SELECT quantity FROM owned_stock WHERE cust_id={user_id} AND stock_id={stock_id}"
    cursor.execute(get_quantity)
    quan_current = cursor.fetchone()
    
    if quan_current:
        quan_current = quan_current[0]  # Extract the quantity from the tuple
    else:
        quan_current = 0  # If no records, assume 0 shares owned

    # Handle stock transaction logic here
    if action == 'buy':
        if quan_current == 0:
            get_stock_name = f"SELECT comp_name FROM company_detail WHERE comp_id={stock_id}"
            cursor.execute(get_stock_name)
            stock_name = cursor.fetchone()
            if stock_name:
                stock_name = stock_name[0]
            else:
                return "No company is registered with the following id", 400
            insert_query = f"INSERT INTO owned_stock(cust_id, stock_name, stock_id, quantity) VALUES ({user_id}, '{stock_name}', {stock_id}, {quantity})"
            cursor.execute(insert_query)
            con.commit()
        else:
            updated_quan = (quan_current or 0) + quantity  # Use `or 0` to ensure no NoneType issues
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)
            con.commit()
            print(f"Buying {quantity} shares of Stock ID: {stock_id}")

    elif action == 'sell':
        if quan_current > 0 and quan_current >= quantity:  # Check if there are enough stocks to sell
            updated_quan = quan_current - quantity
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)
            con.commit()
            print(f"Selling {quantity} shares of Stock ID: {stock_id}")
        else:
            return "Not enough stocks owned to sell", 400

    else:
        return "Unknown action", 400

    # Get updated stock data from the database
    data = get_owned_stock_data()
    return render_template('user_table.html', stocks=data)
    # Get stock data from the database
    # response = make_response(render_template('user_table.html', stocks=data))

    # # Disable caching for dynamic content
    # response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # response.headers['Pragma'] = 'no-cache'
    # response.headers['Expires'] = '0'
    
    # return response

# Route for the third page (another page in the navbar)
@app.route('/profile')
def another_page():
    
    return render_template('another_page.html')




@app.route('/owned-table')
def owned_page():
    data=get_owned_stock_data()
    return render_template('owned_table.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
