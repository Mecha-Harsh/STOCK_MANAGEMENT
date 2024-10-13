from createdatabase import set_database

cursor,con = set_database()

if cursor:
    cursor.execute("SELECT company_name FROM company")
    company_names = cursor.fetchall()
    cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
    current_names = {col[0] for col in cursor.fetchall()} 
    required_value=[]
    for company in company_names:
        for name in company:
            if name not in current_names:
                required_value.append(name)
                query = f"ALTER TABLE stock_price ADD COLUMN `{name}` VARCHAR(100)"
                cursor.execute(query)
    con.commit()
    

    recent_time_query = "SELECT date_time FROM stock_price ORDER BY date_time DESC LIMIT 1"
    cursor.execute(recent_time_query)
    recent = cursor.fetchone()
    
    
    # cursor.execute("SELECT * FROM company")
    # rows = cursor.fetchall()
    
    #column_names = ', '.join(f"{name}" for name in required_value)  # Format column names with backticks
    for i in required_value:
        fetch_query = f"SELECT company_name, stock_price from company where company_name = '{i}'"
        cursor.execute(fetch_query)
        rows = cursor.fetchall()
        print(rows)

        if recent:
            recent_time = recent[0]
            for row in rows:

                if isinstance(row[1], str): 
                    insert_value = f"UPDATE stock_price SET {row[0]} = '{row[1]}' WHERE date_time = '{recent_time}'"
                else:
                    insert_value = f"UPDATE stock_price SET {row[0]} = {row[1]} WHERE date_time = '{recent_time}'"
                cursor.execute(insert_value)
            con.commit()
        else:
            print("No recent date_time found.")

        
