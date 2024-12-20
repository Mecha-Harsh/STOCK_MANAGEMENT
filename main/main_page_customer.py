from flask import Flask, jsonify, render_template, request, make_response, url_for, redirect
from stock_update import get_data, get_owned_stock_data, get_data_for_owned_stock_page, get_stock_of_company
from createdatabase import set_database
import sys
import webbrowser
from datetime import datetime

# Initialize the database connection
cursor, con = set_database()

# Example user ID, to be replaced with the ID of the logged-in user
user_id = int(sys.argv[1]) if len(sys.argv) > 1 else None

def fetch_latest_price(comp_id):    
    # query = f"SELECT comp_name FROM company_detail WHERE comp_id = {comp_id}"
    # cursor.execute(query)
    # result = cursor.fetchone()
    result=1
    
    if result:
        # name = result[0]
        price_query = f"SELECT price FROM stock_price where stock_id={comp_id} ORDER BY date_time DESC LIMIT 1"
        cursor.execute(price_query)
        price_result = cursor.fetchone()
        
        if price_result:
            return price_result[0]
        else:
            print("No price data found for the specified company.")
            return None
    else:
        print("Company not found with the given comp_id.")
        return None

app = Flask(__name__)

@app.route('/')
def index():
    random_num = 42
    return render_template('main.html', random_num=random_num)

@app.route('/stock-table')
def stock_table():
    stocks = get_data()
    response = make_response(render_template('table.html', stocks=stocks))
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

@app.route('/submit-transaction', methods=['POST'])
def submit_transaction():
    stock_id = int(request.form.get('stock_id'))
    quantity = int(request.form.get('quantity'))
    action = request.form.get('action')
    
    get_quantity_query = f"SELECT quantity FROM owned_stock WHERE cust_id={user_id} AND stock_id={stock_id}"
    cursor.execute(get_quantity_query)
    quan_current = cursor.fetchone()
    curren_price = fetch_latest_price(stock_id)
    
    avialable_stock_query = f"SELECT stock_quantity FROM company_transac WHERE stock_id = {stock_id} ORDER BY Date_Time DESC LIMIT 1"
    cursor.execute(avialable_stock_query)
    avl_stock = cursor.fetchone()

    # Check if avl_stock has a value before accessing it
    if avl_stock:
        avl_stock = avl_stock[0]
    else:
        query = f"SELECT initial_stock FROM stock_initial WHERE stock_id = {stock_id}"
        cursor.execute(query)
        temp = cursor.fetchone()
        avl_stock = temp[0] if temp else 0  # Default to 0 if no initial stock found
    
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
        
        stock_left = avl_stock - quantity
        
        trans_company = f"""
        INSERT INTO company_transac(comp_id, stock_id, stock_quantity, transac_type, transac_quantity, price, total_price) 
        VALUES ({stock_id}, {stock_id}, {stock_left}, "bought", {quantity}, {curren_price}, {curren_price * quantity})
        """
        cursor.execute(trans_company)
        con.commit()
        
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
            
            stock_left = avl_stock + quantity
        
            trans_company = f"""
            INSERT INTO company_transac(comp_id, stock_id, stock_quantity, transac_type, transac_quantity, price, total_price) 
            VALUES ({stock_id}, {stock_id}, {stock_left}, "sold", {quantity}, {curren_price}, {curren_price * quantity})
            """
            cursor.execute(trans_company)
            con.commit()
            
        else:
            return "Not enough stocks owned to sell", 400

    else:
        return "Unknown action", 400

    data = get_owned_stock_data(user_id)
    return render_template('user_table.html', stocks=data)

@app.route('/profile')
def another_page():
    trans = []
    query = f"SELECT * FROM customer WHERE cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchone()
    data = {
        'id': rows[0],
        'name': rows[1],
        'email': rows[2],
        'phone': rows[3],
        'age': rows[5],
        'gender': rows[6]
    }
    
    query = f"SELECT * FROM customer_transac WHERE cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        value_1 = {
            'trans_id': row[0],
            'stock_id': row[2],
            'action': row[3],
            'quantity': row[4],
            'date_time': row[5].strftime('%Y-%m-%d %H:%M:%S'),            
            'price': row[6],
            'total_value': row[7]
        }
        trans.append(value_1)
    return render_template('user_profile.html', user_info=data, transaction=trans)

@app.route('/owned-Stocks')
def owned_page():
    data = get_data_for_owned_stock_page(user_id)
    return render_template('owned_table.html', stocks=data)

@app.route('/api/stock-data')
def api_stock_data():
    stock_id = request.args.get('stock')
    stocks = get_stock_of_company(stock_id)
    
    if not stocks:
        return jsonify({'error': 'No stock data found'}), 404

    stock_data = [{'date': stock['date'], 'price': stock['price']} for stock in stocks]
    stock_data = stock_data[-10:]

    print(f"API Stock Data: {stock_data}")
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

    print(f"Graph Data: {dates}, {prices}")
    return render_template('stock_graph.html', stock_id=stock_id, dates=dates, prices=prices)

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if user_id:
        cursor.execute("DELETE FROM customer WHERE cust_id = %s", (user_id,))
        con.commit()
        webbrowser.open_new(('http://127.0.0.1:5000/'))
    return "Error: User not found", 404

if __name__ == '__main__':
    app.run(debug=False, port=5002)
