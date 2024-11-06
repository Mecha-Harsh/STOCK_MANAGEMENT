import random 
import time
from datetime import datetime
from createdatabase import set_database

# Set up database connection
cursor, con = set_database()

ids = []
cursor.execute("SELECT comp_id FROM company_detail")
ok = cursor.fetchall()
for i in ok:
    ids.append(i[0])



def update_stock():
    print(ids)
    rows = []
    for i in ids:
        fquey = f"SELECT price FROM stock_price WHERE stock_id = {i} ORDER BY date_time DESC"
        cursor.execute(fquey)
        temp = cursor.fetchone()
        cursor.fetchall()  # Fetch any remaining rows to clear the result buffer
        print(temp)
        if temp:  # Ensure there is a result before accessing temp[0]
            rows.append(temp[0])
    
    print(rows)
    
    if rows:
        cursor.execute("SHOW COLUMNS FROM stock_price")
        columns = cursor.fetchall()
        column_names = [f"`{column[0]}`" for column in columns[1:]]  # Skip the first column (date_time)

        values = []
        for num in rows:
            num = int(num)
            sign = random.randint(0, 2)
            ran = int(num / 10)
            rand_value = random.randint(0, ran)
            if sign == 0:
                num += rand_value
            else:
                num -= rand_value
            values.append(num)

        values = [int(val) for val in values]

        for i in range(len(ids)):
            insert_fetxh = f"INSERT INTO stock_price (stock_id, price) VALUES ({ids[i]}, {values[i]})"
            cursor.execute(insert_fetxh)
            con.commit()
    else:
        print("No rows found in stock_price.")
    return rows

# def get_data():
#     data = []
#     names = []
#     prices = update_stock()
#     min_values = []
#     max_values = []
#     comp_id = []
#     if cursor:
#         cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
#         column_names = cursor.fetchall()
#         relevant_column_names = []

#         for name in column_names:
#             if name[0] != "date_time":
#                 relevant_column_names.append(name)
#         print(relevant_column_names)
        
#         for column_name in relevant_column_names:
#             names.append(column_name)

#             query_min = f"SELECT MIN FROM stock where stock_id = {1}"
#             cursor.execute(query_min)
#             min_value = cursor.fetchone()
#             min_values.append(min_value[0])

#             query_max = f"SELECT MAX(`{column_name[0]}`) FROM stock_price"
#             cursor.execute(query_max)
#             max_value = cursor.fetchone()
#             max_values.append(max_value[0])

#         print(names)
#         for i in names:
#             print(i[0])
#             query = "SELECT comp_id FROM company_detail WHERE comp_name = %s"
#             cursor.execute(query, (i[0],))
#             temp = cursor.fetchone()
#             comp_id.append(temp[0])

#         for i in range(len(names)):
#             value = {
#                 "id": comp_id[i],
#                 "name": names[i][0],
#                 "price": prices[i] if len(prices) > 0 else None,
#                 "min": min_values[i],
#                 "max": max_values[i]
#             }
#             data.append(value)
#     else:
#         print("No data found in stock_price table.")
    
#     return data

 


def get_data():
    data=[]
    names=[]
    max_values=[]
    min_values=[]
    prices = update_stock()
    for id in ids:
        query = f"Select comp_name from company_detail where comp_id = {id}"
        cursor.execute(query)
        name=cursor.fetchone()
        names.append(name[0])
    for id in ids:
        max_quer=f"Select MAX(price) from stock_price where stock_id ={id} GROUP BY stock_id"
        cursor.execute(max_quer)
        max=cursor.fetchone()
        max_values.append(max[0])
        min_query=f"Select MIN(price) from stock_price where stock_id ={id} GROUP BY stock_id"
        cursor.execute(min_query)
        min=cursor.fetchone()
        min_values.append(min[0])
    for i in range(len(ids)):
        value = {
                "id": ids[i],
                "name": names[i],
                "price": prices[i] if len(prices) > 0 else None,
                "min": min_values[i],
                "max": max_values[i]
            }
        data.append(value)
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
        fetch_price=f"select price from stock_price where stock_id={user_id} order by date_time desc limit 1"
        cursor.execute(fetch_price)
        price=cursor.fetchone()
        current_value = price[0]
        
        
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
    # query = f"SELECT comp_name FROM company_detail WHERE comp_id = {comp_id}"
    # cursor.execute(query)
    # name = cursor.fetchone()
    # name = name[0]  # Assuming comp_name is the only element returned
    price_query = f"SELECT price,date_time FROM stock_price where stock_id={comp_id}"
    cursor.execute(price_query)
    prices = cursor.fetchall()
    print(prices)
    max=-9999999
    min=99999999
    if prices:
        for row in prices:
            if(row[0]==None):
                continue
            if(max<row[0]):
                max=row[0]
            if(min>row[0]):
                min=row[0]
            temp = {
                "date": row[1].strftime('%Y-%m-%d %H:%M:%S'),  # Format the date
                "price": row[0],
                "min":min,
                "max":max
            }
            data.append(temp)
    else:
        print("No rows found")
    return data




def get_stock_of_company_for_graph(comp_id):
    data = []
    a = update_stock()  # Assuming this updates the stock prices
    # query = f"SELECT comp_name FROM company_detail WHERE comp_id = {comp_id}"
    # cursor.execute(query)
    # name = cursor.fetchone()
    # name = name[0]  # Assuming comp_name is the only element returned
    price_query = f"SELECT price,date_time FROM stock_price where stock_id={comp_id}"
    cursor.execute(price_query)
    prices = cursor.fetchall()
    print(prices)
    max=-9999999
    min=99999999
    if prices:
        for row in prices:
            if(row[0]==None):
                continue
            if(max<row[0]):
                max=row[0]
            if(min>row[0]):
                min=row[0]
            temp = {
                "date": row[1].strftime('%Y-%m-%d %H:%M:%S'),  # Format the date
                "price": row[0],
                "min":min,
                "max":max
            }
            data.append(temp)
    else:
        print("No rows found")
    return data


if __name__ == "__main__":
    #get_data()
    get_data_for_owned_stock_page(1)
    # print(get_stock_of_company(2))
    # print(get_data_for_owned_stock_page(1))
    update_stock()
    # print(get_owned_stock_data(1))
    # print(get_data())