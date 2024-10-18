import random 
import time
from createdatabase import set_database

# Set up database connection
cursor, con = set_database()

if cursor:
    data = []
    prices = []
    relevant_column_names = []
    names=[]
    min_values = []
    max_values = []
    cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
    rows = cursor.fetchone()
    cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
    column_names = cursor.fetchall()
    relevant_column_names = []
    for name in column_names:
        if name[0]!="date_time":
            relevant_column_names.append(name)
    for column_name in relevant_column_names:
        names.append(column_name)
    print(names)
    
    if rows:
        # Fetch column names from the stock_price table
        cursor.execute("SHOW COLUMNS FROM stock_price")
        columns = cursor.fetchall()
        column_names = [f"`{column[0]}`" for column in columns[1:]]  # Skip the first column (date_time) and add backticks
        value = []
        for num in rows[1:]:  # Skip the first column (date_time)
            num = int(num)  # Ensure the number is an integer
            sign = random.randint(0, 2)
            ran = int(num / 10)
            rand_value = random.randint(0, ran)  # Generate a random number
            if sign == 0:
                num = num + rand_value  # Add random value
            else:
                num = num - rand_value  # Subtract random value
            
            value.append(num)  # Append modified value
            
        # Ensure all values are integers
        value = [int(val) for val in value]

        # Create placeholders for SQL INSERT
        placeholders = ', '.join(['%s'] * len(value))
        insert_fetch = f"INSERT INTO stock_price ({', '.join(column_names)}) VALUES ({placeholders})"
        
        # Execute the INSERT statement with the new values
        cursor.execute(insert_fetch, value)
        con.commit()  # Commit the transaction
        print(value)
    else:
        print("No rows found in stock_price.")
    
    
    
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
            value1 = {
                "name": names[i][0],
                "price": prices[0][i] if len(prices) > 0 else None,
                "min": min_values[i],
                "max": max_values[i]
            }
            data.append(value1)
        print(data)
    
    
    













# Close the connection if it is open
if con and con.is_connected():
    con.close()
