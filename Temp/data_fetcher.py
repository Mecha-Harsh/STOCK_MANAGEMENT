from createdatabase import set_database
import time

# Set up the database connection
cursor, con = set_database()

while True:
    if cursor:
        # Fetch the most recent row of the stock_price table
        cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
        rows = cursor.fetchall()
        
        if rows:
            # Print the latest stock prices
            latest_stock_prices = rows[0][1:]  # Skip the date_time column
            print("Latest Stock Prices:")
            for price in latest_stock_prices:
                print(price)
        else:
            print("No stock data found.")
        
    else:
        print("Cursor is not available.")

    time.sleep(10)  # Wait for 10 seconds before fetching again
