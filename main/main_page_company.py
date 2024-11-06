from flask import Flask, render_template, request, make_response, jsonify
from stock_update import get_data, get_owned_stock_data, get_data_for_owned_stock_page, get_stock_of_company,get_stock_of_company_for_graph
from createdatabase import set_database
import sys
import webbrowser
import threading

# Set up database connection
cursor, con = set_database()

company_id = int(sys.argv[1]) if len(sys.argv) > 1 else None

app = Flask(__name__)

@app.route('/')
def index():
    random_num = 41  # Can generate dynamically if needed
    return render_template('main1.html', random_num=random_num)

@app.route('/stock-table')
def stock_table():
    stocks = get_data()  # Get stock data from the database
    response = make_response(render_template('table.html', stocks=stocks))
    
    # Disable caching for dynamic content
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

@app.route('/listed-stocks-table')
def listed_stock_table():
    data = get_stock_of_company_for_graph(company_id)
    return render_template('comp_stock_table.html', stocks=data)

@app.route('/listed-stocks')
def listed_stock():
    return render_template('company_listed_stock.html')

@app.route('/api/stock-data')
def api_stock_data():
    stocks = get_stock_of_company(company_id)  # Fetch stock data for the graph
    stock_data = [{'date': stock['date'], 'price': stock['price']} for stock in stocks]

    # Show only the last 10 entries
    stock_data = stock_data[-10:]
    
    return jsonify(stock_data)


@app.route('/profile')
def profile():
    query = f"select * from company_detail where comp_id={company_id}"
    cursor.execute(query)
    user_data_tuple = cursor.fetchone()
    user_data_dict = {
        'id': user_data_tuple[0],
        'name': user_data_tuple[1],
        'email': user_data_tuple[2],
        'phone': user_data_tuple[3],
        'age': user_data_tuple[4]
    }
    return render_template('company_profile.html',user_info=user_data_dict)
if __name__ == '__main__':

    app.run(debug=False, port=5001)
