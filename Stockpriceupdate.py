import random 
import time
from createdatabase import set_database

cursor, con = set_database()

if cursor:
    while True:
        cursor.execute("SELECT * FROM stock_price ORDER BY date_time DESC LIMIT 1")
        rows = cursor.fetchone()
        if rows:
            cursor.execute("SHOW COLUMNS FROM stock_price")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns[1:]]  

            value = []
            for num in rows[1:]:  # Skip the first column (date_time)
                num=int(num)
                sign = random.randint(0, 2)
                ran = int(num/10)
                rand_value = random.randint(0,ran)  # Generate a random number
                if sign == 0:
                    num = num + rand_value  # Add random value
                else:
                    num = num - rand_value  # Subtract random value
                value.append(num)  # Append modified value
                 

            # Create placeholders for SQL INSERT
            placeholders = ', '.join(['%s'] * len(value))
            insert_fetch = f"INSERT INTO stock_price ({', '.join(column_names)}) VALUES ({placeholders})"
            
            # Execute the INSERT statement with the new values
            cursor.execute(insert_fetch, value)
            con.commit()  # Commit the transaction
            print(value)
        else:
            print("No rows found in stock_price.")
        
        time.sleep(20)  # Wait for 10 seconds before the next iteration

# Close the connection at the end (if you ever exit the loop)
if con and con.is_connected():
    con.close()
