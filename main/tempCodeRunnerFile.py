    query = f"select * from customer where cust_id={user_id}"
    cursor.execute(query)
    rows = cursor.fetchone()