from createdatabase import set_database

cursor, con = set_database()

if cursor:
    current_ids_query = "SELECT DISTINCT stock_id FROM stock_price"
    cursor.execute(current_ids_query)
    current_ids = cursor.fetchall()  # Fetch all rows to get all distinct IDs
    current_ids = [row[0] for row in current_ids]  # Extract the IDs into a list
    
    id_in_company_detail_query = "SELECT DISTINCT stock_id FROM stock_initial"
    cursor.execute(id_in_company_detail_query)
    ids_in_comp_detail = cursor.fetchall()  # Fetch all rows for IDs in stock_initial
    ids_in_comp_detail = [row[0] for row in ids_in_comp_detail]

    for stock_id in ids_in_comp_detail:
        if stock_id not in current_ids:
            fetch_price_query = f"SELECT stock_price FROM stock_initial WHERE stock_id = {stock_id}"
            cursor.execute(fetch_price_query)
            price = cursor.fetchone()
            price = price[0]

            insert_query = f"INSERT INTO stock_price (stock_id, price) VALUES ({stock_id}, {price})"
            cursor.execute(insert_query)
            print(stock_id, price)
            con.commit()

    print("IDs in stock_price:", current_ids)
    print("IDs in stock_initial:", ids_in_comp_detail)
