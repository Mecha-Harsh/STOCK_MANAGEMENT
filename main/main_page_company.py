from flask import Flask, render_template, request, make_response, jsonify
from stock_update_final import get_data, get_owned_stock_data, get_data_for_owned_stock_page, get_stock_of_company
from createdatabase import set_database

cursor, con = set_database()

company_id = 1

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
    data = get_stock_of_company(company_id)
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
