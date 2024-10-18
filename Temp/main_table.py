from createdatabase import set_database
from flask import Flask, render_template
from stock_update_final import get_data
cursor, con = set_database()
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('main.html')

from flask import make_response

@app.route('/stock-table')
def stock_table():
    
    stocks = get_data()
    response = make_response(render_template('table.html', stocks=stocks))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(debug=True)

