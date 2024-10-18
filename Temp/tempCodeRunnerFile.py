from createdatabase import set_database
from flask import Flask, render_template
cursor, con = set_database()
app = Flask(__name__)

def get_data():
    data = []
    names = []
    prices = []
    min_values = []
    max_values = []
    if cursor:
        # Fetch the most recent row of the stock_price table
        cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
        data_temp = cursor.fetchall()
        if data_temp:  # Check if there's any data
            # Append all values except the first column (date_time)
            for i in data_temp:
                rev = i[1:]  # Skip the first column (date_time)
                prices.append(rev)  # prices will now be a list of tuples
            # Fetch column names from the stock_price table
            cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
            column_names = cursor.fetchall()
            relevant_column_names = []

            for name in column_names:
                if name[0]!="date_time":
                    relevant_column_names.append(name)
            for column_name in relevant_column_names:
                names.append(column_name)

                query_min = f"SELECT MIN(`{column_name[0]}`) FROM stock_price"
                cursor.execute(query_min)
                min_value = cursor.fetchone()  # Use fetchone to get a single row
                min_values.append(min_value[0])  # Append the minimum value

                # Get the maximum value for the current column
                query_max = f"SELECT MAX(`{column_name[0]}`) FROM stock_price"
                cursor.execute(query_max)
                max_value = cursor.fetchone()  # Use fetchone to get a single row
                max_values.append(max_value[0])  # Append the maximum value

            # Create a data structure for output
            for i in range(len(names)):
                value = {
                    "name": names[i][0],
                    "price": prices[0][i] if len(prices) > 0 else None,
                    "min": min_values[i],
                    "max": max_values[i]
                }
                data.append(value)
        else:
            print("No data found in stock_price table.")
    else:
        print("Cursor is not available.")

    print("Fetched data:", data)  # Debugging line to check the fetched data
    return data

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
