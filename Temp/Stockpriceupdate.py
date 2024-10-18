import random 
import time
from createdatabase import set_database

cursor, con = set_database()

ans=[]

def get_value():
    return ans
    

if cursor:
    while True:
        cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
        rows = cursor.fetchall()
        if rows:
            # Fetch all column names, skipping the first column (e.g., date_time)
            cursor.execute("SHOW COLUMNS FROM stock_price")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns[1:]]  # Skip the 'date_time' column

            # Verify column names and their count
            # Prepare values for the INSERT query
            value = []
            for num in rows[0][1:]:  # Iterate over all but the first column (date_time)
                num = int(num)
                sign = random.randint(0, 1)
                ran = int(num / 10)
                rand_value = random.randint(0, ran)
                num = num + rand_value if sign == 0 else num - rand_value
                value.append(num)

            # Ensure the value list matches the number of columns (excluding date_time)
            if len(column_names) != len(value):
                print("Mismatch in column names and values count")
                break

            # Create placeholders for SQL INSERT with backticks for column names
            column_names_quoted = ', '.join([f'`{col}`' for col in column_names])
            placeholders = ', '.join(['%s'] * len(value))
            insert_fetch = f"INSERT INTO stock_price ({column_names_quoted}) VALUES ({placeholders})"
            # print(value)

            # Execute the INSERT statement with the values
            cursor.execute(insert_fetch, value)
            con.commit()  # Commit the transaction        
        else:
            print("No stock has been listed yet.")
        ans=value
        time.sleep(10)  # Wait for 20 seconds before the next iteration

# Close the connection at the end (if you ever exit the loop)
if con and con.is_connected():
    con.close()
