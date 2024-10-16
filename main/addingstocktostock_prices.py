from createdatabase import set_database

cursor,con = set_database()

if cursor:
    cursor.execute("SELECT comp_name,comp_id FROM company_detail")
    company_names = cursor.fetchall()
    cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
    current_names = {col[0] for col in cursor.fetchall()} 
    required_value=[]
    required_id=[]
    #print(company_names)
    
    for company in company_names:
        if company[0] not in current_names:
            query = f"ALTER TABLE stock_price ADD COLUMN `{company[0]}` VARCHAR(100)"
            required_value.append(company[0])
            required_id.append(company[1])
            cursor.execute(query)
        con.commit()
    
    

    recent_time_query = "SELECT date_time FROM stock_price ORDER BY date_time DESC LIMIT 1"
    cursor.execute(recent_time_query)
    recent = cursor.fetchone()
    
    
    cursor.execute("SELECT * FROM company")
    rows = cursor.fetchall()
        
    column_names = ', '.join(f"{name}" for name in required_value)  # Format column names with backticks
    for i in required_id:
        fetch_query = "SELECT cd.comp_name, si.stock_price FROM company_detail AS cd JOIN stock_initial AS si ON cd.comp_id = si.comp_id WHERE cd.comp_id = %s"
        cursor.execute(fetch_query, (i,))
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

        
