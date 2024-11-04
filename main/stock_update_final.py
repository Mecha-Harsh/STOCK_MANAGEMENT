import random 
import time
from datetime import datetime
from createdatabase import set_database

# Set up database connection
cursor, con = set_database()

def update_stock():
    value = []
    if cursor:
        # Fetch the latest row from the stock_price table
        cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
        rows = cursor.fetchone()
        
        if rows:
            # Fetch column names from the stock_price table
            cursor.execute("SHOW COLUMNS FROM stock_price")
            columns = cursor.fetchall()
            column_names = [f"`{column[0]}`" for column in columns[1:]]  # Skip the first column (date_time) and add backticks

            for num in rows[1:]:  # Skip the first column (date_time)
                num = int(num)  # Ensure the number is an integer
                sign = random.randint(0, 2)
                ran = int(num / 10)
                rand_value = random.randint(0, ran)  # Generate a random number
                if sign == 0:
                    num += rand_value  # Add random value
                else:
                    num -= rand_value  # Subtract random value
                
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
        return value

def get_data():
    data = []
    names = []
    prices = update_stock()
    min_values = []
    max_values = []
    comp_id = []
    if cursor:
        cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
        column_names = cursor.fetchall()
        relevant_column_names = []

        for name in column_names:
            if name[0] != "date_time":
                relevant_column_names.append(name)
        print(relevant_column_names)
        
        for column_name in relevant_column_names:
            names.append(column_name)

            query_min = f"SELECT MIN(`{column_name[0]}`) FROM stock_price"
            cursor.execute(query_min)
            min_value = cursor.fetchone()
            min_values.append(min_value[0])

            query_max = f"SELECT MAX(`{column_name[0]}`) FROM stock_price"
            cursor.execute(query_max)
            max_value = cursor.fetchone()
            max_values.append(max_value[0])

        print(names)
        for i in names:
            print(i[0])
            query = "SELECT comp_id FROM company_detail WHERE comp_name = %s"
            cursor.execute(query, (i[0],))
            temp = cursor.fetchone()
            comp_id.append(temp[0])

        for i in range(len(names)):
            value = {
                "id": comp_id[i],
                "name": names[i][0],
                "price": prices[i] if len(prices) > 0 else None,
                "min": min_values[i],
                "max": max_values[i]
            }
            data.append(value)
    else:
        print("No data found in stock_price table.")
    
    return data

def get_owned_stock_data(user_id):
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

def get_data_for_owned_stock_page(user_id):
    cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
    column_names = cursor.fetchall()
    relevant_column_names = [name for name in column_names if name[0] != "date_time"]

    final_data = []
    user_data = get_owned_stock_data(user_id)
    query = f"SELECT stock_id, each_stock_price, transac_type, transac_quantity, total_price FROM customer_transac WHERE cust_id = {user_id}"
    cursor.execute(query)
    transactions = cursor.fetchall()
    
    for stock in user_data:
        bought_price = 0
        each_price = 0

        for transac in transactions:
            stock_id, each_stock_price, transac_type, transac_quantity, total_price = transac
            
            if stock["id"] == stock_id:
                if transac_type == "bought":
                    bought_price += total_price
                    each_price = each_stock_price
                elif transac_type == "sold":
                    bought_price -= each_price * transac_quantity
        
        stock["bought_price"] = bought_price
        
        # Calculate the current value based on the latest price
        current_values = update_stock()
        count = 0
        current_value = None
        for names in relevant_column_names:
            if names[0] != stock["name"]:
                count += 1
            else:
                current_value = current_values[count]
                break
        
        if current_value is not None:
            stock["current_price"] = current_value * stock["quantity"]
        else:
            stock["current_price"] = 0
        
        final_data.append(stock)
        print(final_data)
    
    return final_data




def get_stock_of_company(comp_id):
    data = []
    a = update_stock()  # Assuming this updates the stock prices
    query = f"SELECT comp_name FROM company_detail WHERE comp_id = {comp_id}"
    cursor.execute(query)
    name = cursor.fetchone()
    name = name[0]  # Assuming comp_name is the only element returned
    price_query = f"SELECT date_time, {name} FROM stock_price"
    cursor.execute(price_query)
    prices = cursor.fetchall()
    max=-9999999
    min=99999999
    if prices:
        for row in prices:
            if(row[1]==None):
                continue
            if(max<row[1]):
                max=row[1]
            if(min>row[1]):
                min=row[1]
            temp = {
                "date": row[0].strftime('%Y-%m-%d %H:%M:%S'),  # Format the date
                "price": row[1],
                "min":min,
                "max":max
            }
            data.append(temp)
    else:
        print("No rows found")
    return data


if __name__ == "__main__":
    #get_data()
    #get_data_for_owned_stock_page(1)
    get_stock_of_company(2)