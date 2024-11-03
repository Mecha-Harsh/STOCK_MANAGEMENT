import subprocess
import time
from createdatabase import set_database

cursor,con = set_database()

# ans=[]

# def get_data():
#     names = []
#     prices = []
#     data = []
#     min_values = []
#     max_values = []
#     if cursor:
#         # Fetch the most recent row of the stock_price table
#         cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
#         data_temp = cursor.fetchall()
        
#         # Append all values except the first column (date_time)
#         for i in data_temp:
#             rev = i[1:]  # Skip the first column (date_time)
#             prices.append(rev)  # prices will now be a list of tuples

#         # Fetch column names from the stock_price table
#         cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
#         column_names = cursor.fetchall()
#         relevant_column_names=[]

#         for index, name in enumerate(column_names):
#             if index > 0:  # Skip the first column (index 0)
#                 relevant_column_names.append(name[0])

#         for column_name in relevant_column_names:
#             names.append(column_name)

#             query_min = f"SELECT MIN(`{column_name}`) FROM stock_price"
#             cursor.execute(query_min)
#             min_value = cursor.fetchone()  # Use fetchone to get a single row
#             min_values.append(min_value[0])  # Append the minimum value

#             # Get the maximum value for the current column
#             query_max = f"SELECT MAX(`{column_name}`) FROM stock_price"
#             cursor.execute(query_max)
#             max_value = cursor.fetchone()  # Use fetchone to get a single row
#             max_values.append(max_value[0])  # Append the maximum value

#         # Create a data structure for output
#         for i in range(len(names)):
#             value = {
#                 "name": names[i],
#                 "price": prices[0][i] if len(prices) > 0 else None,  
#                 "min": min_values[i],
#                 "max": max_values[i]
#             }
#             data.append(value)
#     return data
user_id =1 
query = f"select * from company_detail where comp_id={1}"
cursor.execute(query)
info = cursor.fetchone()
print(info)


# Start the first process with an infinite loop
#process1 = subprocess.Popen(['python', 'main\\Stockpriceupdate.py'])
# str = r"main\addingstocktostock_prices.py"
# process2 = subprocess.Popen(['python', str])
# process2.wait()
# new_app_path = r'main\main_page_company.py'
# subprocess.Popen(['python',new_app_path])
            # Start the new application on a different port
# subprocess.Popen(['python', new_app_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            # Properly shut down the current Flask application 
# # Start the second process without waiting for the first process to complete
# str = r"main\register_companya.py"
# process2 = subprocess.Popen(['python', str])

# while True:
#     process3=subprocess.Popen(['python','main\Stock_update_2.py'])
#     ans = get_data()
#     time.sleep(20)


# def get_ans():
#     return ans