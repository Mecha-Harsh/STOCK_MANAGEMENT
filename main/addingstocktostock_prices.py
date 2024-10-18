from createdatabase import set_database

cursor, con = set_database()

if cursor:
    # Fetch company names and IDs
    cursor.execute("SELECT comp_name, comp_id FROM company_detail")
    company_names = cursor.fetchall()

    # Fetch current column names in the stock_price table
    cursor.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'stock_price'")
    current_names = {col[0] for col in cursor.fetchall()} 
    required_value = []
    required_id = []

    # Add new columns if they do not exist
    for company in company_names:
        if company[0] not in current_names:
            query = f"ALTER TABLE stock_price ADD COLUMN `{company[0]}` INT"
            required_value.append(company[0])
            required_id.append(company[1])
            cursor.execute(query)
    con.commit()

    # Fetch the most recent date_time
    recent_time_query = "SELECT date_time FROM stock_price ORDER BY date_time DESC LIMIT 1"
    cursor.execute(recent_time_query)
    recent = cursor.fetchone()
    print("Recent date_time:", recent)

    if recent is not None:
        # Update stock prices if recent date_time exists
        recent_time = recent[0]
        for i in required_id:
            fetch_query = "SELECT cd.comp_name, si.stock_price FROM company_detail AS cd JOIN stock_initial AS si ON cd.comp_id = si.comp_id WHERE cd.comp_id = %s"
            cursor.execute(fetch_query, (i,))
            rows = cursor.fetchall()
            print("Fetched rows for update:", rows)

            for row in rows:
                if isinstance(row[1], str):
                    insert_value = f"UPDATE stock_price SET `{row[0]}` = '{row[1]}' WHERE date_time = '{recent_time}'"
                else:
                    insert_value = f"UPDATE stock_price SET `{row[0]}` = {row[1]} WHERE date_time = '{recent_time}'"
                cursor.execute(insert_value)
        con.commit()
    else:
        # If no recent date_time, insert new values
        values_to_insert = []
        column_names = []

        for i in required_id:
            fetch_query = "SELECT cd.comp_name, si.stock_price FROM company_detail AS cd JOIN stock_initial AS si ON cd.comp_id = si.comp_id WHERE cd.comp_id = %s"
            cursor.execute(fetch_query, (i,))
            rows = cursor.fetchall()
            for row in rows:
                column_names.append(f"`{row[0]}`")
                values_to_insert.append(f"'{row[1]}'" if isinstance(row[1], str) else str(row[1]))

        if values_to_insert:  # Check if there are values to insert
            column_names_str = ', '.join(column_names)
            values_to_insert_str = ', '.join(values_to_insert)
            insert_query = f"INSERT INTO stock_price ({column_names_str}) VALUES ({values_to_insert_str})"
            cursor.execute(insert_query)
            con.commit()
