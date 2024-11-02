if cursor:
            try:
                cursor.execute(sql_value)
                conn.commit()
                
                cursor.execute(get_compid)
                compid = cursor.fetchall()
                compid=compid[0]
                if compid:
                    print(f"Company ID fetched: {compid[0]}")
                else:
                    print("No company ID found for the given details.")
                
            except Exception as e:
                print(f"Error executing query: {e}")
                return "Internal Server Error", 500
        else:
            print("No connection found")
            return "Database Connection Error", 500