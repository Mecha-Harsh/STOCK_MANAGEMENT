import mysql.connector

def create_connection():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="harsh@125",
        connection_timeout=600
    )
    return con
    
def set_database():
    con = create_connection()
    
    # Check if the connection was successful
    if con is None:
        print("Connection failed!")
        return None, None
    
    cursor = con.cursor()
    
    create_db = "CREATE DATABASE IF NOT EXISTS stock_exp"
    
    create_table_stock_price = """
    CREATE TABLE IF NOT EXISTS stock_price (
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    create_company_data = """
    CREATE TABLE IF NOT EXISTS company_detail (
        comp_id INT PRIMARY KEY AUTO_INCREMENT,
        comp_name VARCHAR(100) UNIQUE,
        email VARCHAR(100),
        phone_no VARCHAR(15),
        address VARCHAR(100)
    )
    """
    
    create_initial_stock_prices = """
    CREATE TABLE IF NOT EXISTS stock_initial (
        comp_id INT,
        stock_id INT DEFAULT NULL,
        gross_expense INT,
        gross_income INT,
        stock_price INT,
        FOREIGN KEY (comp_id) REFERENCES company_detail(comp_id),
        UNIQUE KEY (stock_id)  
    )
    """
    
    # Trigger to set stock_id to the same value as comp_id after insert
    
    create_table_customer = """
    CREATE TABLE IF NOT EXISTS customer (
        cust_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,          
        phone VARCHAR(15),
        password VARCHAR(255) NOT NULL,
        age INT,
        gender VARCHAR(10)
    )
    """
    
    create_company_transaction_table="""
    CREATE TABLE company_transac (
    comp_transac_no INT PRIMARY KEY AUTO_INCREMENT,
    comp_id INT,
    stock_id INT,
    transac_type VARCHAR(10),
    transac_quantity INT,
    Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity_before INT,
    quantity_after INT,
    price_at_transac DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (comp_id) REFERENCES Company(Company_ID),
    FOREIGN KEY (stock_id) REFERENCES Stock(Stock_ID)
    );
    """

    
    create_owned_stock = """
    CREATE TABLE IF NOT EXISTS owned_stock (
        cust_id INT,
        stock_name VARCHAR(100),
        stock_id INT,
        quantity INT
    )
    """
    
    create_customer_transac = """
    CREATE TABLE IF NOT EXISTS customer_transac (
        cust_transac_no INT PRIMARY KEY AUTO_INCREMENT,
        cust_id INT,
        stock_id INT,
        transac_type VARCHAR(50),
        transac_quantity INT,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        each_stock_price INT,
        total_price INT,
        FOREIGN KEY (cust_id) REFERENCES customer(cust_id),
        FOREIGN KEY (stock_id) REFERENCES stock_initial(stock_id)
    )
    """
    
    # Execute SQL commands
    cursor.execute(create_db)  # Create the database
    cursor.execute("USE stock_exp")  # Switch to the new database
    cursor.execute(create_table_stock_price)  # Create tables
    cursor.execute(create_company_data)
    cursor.execute(create_initial_stock_prices)
    cursor.execute(create_table_customer)
    cursor.execute(create_owned_stock)
    cursor.execute(create_customer_transac)
    return cursor, con

if __name__ == "__main__":
    cursor, con = set_database()
    
    # Check if the connection was established
    if con is not None and con.is_connected():
        con.close()
        print("The connection is closed")
