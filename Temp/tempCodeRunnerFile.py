def submit_transaction():
    stock_id = int(request.form.get('stock_id'))  # Get stock ID from form and convert to integer
    quantity = int(request.form.get('quantity'))   # Get quantity from form and convert to integer
    action = request.form.get('action')             # Get action (buy/sell) from button

    get_quantity = f"SELECT quantity FROM owned_stock WHERE cust_id={user_id} AND stock_id={stock_id}"
    cursor.execute(get_quantity)
    quan_current = cursor.fetchone()
    
    if quan_current:
        quan_current = quan_current[0]  # Extract the quantity from the tuple
    else:
        quan_current = 0  # If no records, assume 0 shares owned

    # Handle stock transaction logic here
    if action == 'buy':
        if quan_current==0:
            get_stock_name=f"select comp_name from company_detail where comp_id={stock_id}"
            cursor.execute(get_stock_name)
            stock_name = cursor.fetchone()
            if stock_name:
                stock_name=stock_name[0]
            else:
                return "No company is registered with the following id"
            insert_query = f"Insert into stock_owned(cust_id,stock_name,comp_id,quantity) values ({user_id},'{stock_name}',{stock_id},{quantity})"
            cursor.execute(insert_query)
            con.commit()
        else:
            updated_quan = (quan_current or 0) + quantity  # Use `or 0` to ensure no NoneType issues
            print(update_query)
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)
            con.commit()
            print(f"Buying {quantity} shares of Stock ID: {stock_id}")

    elif action == 'sell':
        if quan_current > 0 and quan_current >= quantity:  # Check if there are enough stocks to sell
            updated_quan = quan_current - quantity
            update_query = f"UPDATE owned_stock SET quantity={updated_quan} WHERE cust_id={user_id} AND stock_id={stock_id}"
            cursor.execute(update_query)
            con.commit()
            print(f"Selling {quantity} shares of Stock ID: {stock_id}")
        else:
            return "Not enough stocks owned to sell", 400

    else:
        return "Unknown action", 400

    # Successful response
    return f'Successfully processed {action} action for Stock ID: {stock_id} with Quantity: {quantity}', 200