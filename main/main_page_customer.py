from flask import Flask, jsonify, render_template, request, make_response,url_for,redirect
from stock_update_final import get_data, get_owned_stock_data, get_data_for_owned_stock_page,get_stock_of_company
from createdatabase import set_database
import sys
from datetime import datetime
# Initialize the database connection
cursor, con = set_database()

# Example user ID, to be replaced with the ID of the logged-in user
user_id=3
#user_id = int(sys.argv[1]) if len(sys.argv) > 1 else None
def fetch_latest_price(comp_id):
    # Fetch the company name based on comp_id
    query = f"SELECT comp_name FROM company_detail WHERE comp_id = {comp_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        name = result[0]
        
        # Use the company name to fetch the latest stock price
        price_query = f"SELECT `{name}` FROM stock_price ORDER BY date_time DESC LIMIT 1"
        cursor.execute(price_query)
        price_result = cursor.fetchone()
        
        if price_result:
            return price_result[0]  # Return the latest price
        else:
            print("No price data found for the specified company.")
            return None
    else:
        print("Company not found with the given comp_id.")
        return None

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    random_num = 42  # Can generate dynamically if needed
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

@app.route('/owned-table')
def owned_table():
    stock = get_data_for_owned_stock_page(user_id)
    print(stock)
    response = make_response(render_template('table_for_owned.html', stocks=stock, random_num=32))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Route for handling stock transactions (buy/sell)
@app.route('/submit-transaction', methods=['POST'])
def submit_transaction():
    stock_id = int(request.form.get('stock_id'))
    quantity = int(request.form.get('quantity'))
    action = request.form.get('action')
    
    get_quantity_query = f"SELECT quantity FROM owned_stock WHERE cust_id={user_id} AND stock_id={stock_id}"
    cursor.execute(get_quantity_query)
    quan_current = cursor.fetchone()
    curren_price = fetch_latest_price(stock_id)
    
    if quan_current:
        quan_current = quan_current[0]
    else:
        quan_current = 0

    if action == 'buy':
        if quan_current == 0:
            get_stock_name = f"SELECT comp_name FROM company_detail WHERE comp_id={stock_id}"
            cursor.execute(get_stock_name)
            stock_name = cursor.fetchone()[0]
            
            insert_query = f"""
            INSERT INTO owned_stock(cust_id, stock_name, stock_id, quantity)
            VALUES ({user_id}, '{stock_name}', {stock_id}, {quantity})
            """
            cursor.execute(insert_query)
        else:
            updated_quan = quan_current + quantity
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)

        transaction_query = f"""
        INSERT INTO customer_transac(cust_id, stock_id, transac_type, transac_quantity, each_stock_price, total_price)
        VALUES ({user_id}, {stock_id}, 'bought', {quantity}, {curren_price}, {curren_price * quantity})
        """
        cursor.execute(transaction_query)
        con.commit()
        print(f"Bought {quantity} shares of Stock ID: {stock_id}")

    elif action == 'sell':
        if quan_current >= quantity:
            updated_quan = quan_current - quantity
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)
            
            transaction_query = f"""
            INSERT INTO customer_transac(cust_id, stock_id, transac_type, transac_quantity, each_stock_price, total_price)
            VALUES ({user_id}, {stock_id}, 'sold', {quantity}, {curren_price}, {curren_price * quantity})
            """
            cursor.execute(transaction_query)
            con.commit()
            print(f"Sold {quantity} shares of Stock ID: {stock_id}")
        else:
            return "Not enough stocks owned to sell", 400

    else:
        return "Unknown action", 400

    data = get_owned_stock_data(user_id)
    return render_template('user_table.html', stocks=data)

# Route for the third page in the navbar
@app.route('/profile')
def another_page():
    trans=[]
    query = f"select * from customer where cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchone()
    data = {
        'id': rows[0],
        'name': rows[1],
        'email': rows[2],
        'phone': rows[3],
        'age': rows[5],
        'gender': rows[6]
        # Password intentionally excluded for security reasons
    }
    
    query = f"select * from customer_transac where cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        value_1 = {
            'trans_id': row[0],
            'stcok_id': row[2],
            'action': row[3],
            'quantity': row[4],
            'date_time': row[5].strftime('%Y-%m-%d %H:%M:%S'),            
            'price': row[6],
            'total_value': row[7]
        }
        trans.append(value_1)
    return render_template('user_profile.html',user_info=data,transaction=trans)

# Route for the owned stocks page
@app.route('/owned-Stocks')
def owned_page():
    data = get_data_for_owned_stock_page(user_id)
    return render_template('owned_table.html', stocks=data)


print(get_data_for_owned_stock_page(1))

@app.route('/api/stock-data')
def api_stock_data():
    stock_id = request.args.get('stock')
    stocks = get_stock_of_company(stock_id)
    
    if not stocks:
        return jsonify({'error': 'No stock data found'}), 404  # Handle empty data

    stock_data = [{'date': stock['date'], 'price': stock['price']} for stock in stocks]
    stock_data = stock_data[-10:]

    print(f"API Stock Data: {stock_data}")  # Debug line
    return jsonify(stock_data)

@app.route('/stock-graph')
def stock_graph():
    stock_id = request.args.get('stock')
    stock_data = get_stock_of_company(stock_id)
    
    
    if not stock_data:
        return render_template('graph.html', stock_id=stock_id, dates=[], prices=[], error='No stock data available')

    graph_data = [{'date': data['date'], 'price': data['price']} for data in stock_data]
    graph_data = graph_data[-10:]

    dates = [data['date'] for data in graph_data]
    prices = [data['price'] for data in graph_data]

    print(f"Graph Data: {dates}, {prices}")  # Debug line
    return render_template('stock_graph.html', stock_id=stock_id, dates=dates, prices=prices)

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if user_id:
        # Execute the deletion logic here, e.g., remove user from the database
        cursor.execute("DELETE FROM customer WHERE cust_id = %s", (user_id,))
        con.commit()
        return redirect(url_for('index'))  # Redirect to home or a confirmation page
    return "Error: User not found", 404



if __name__ == '__main__':
    app.run(debug=False, port=5002)
