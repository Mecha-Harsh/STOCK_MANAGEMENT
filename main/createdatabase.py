import mysql.connector
from mysql.connector import Error
import time

def create_connection():
    """Creates a new MySQL connection."""
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="harsh@125",
            connection_timeout=60000
        )
        return con
    except Error as err:
        print(f"Error: {err}")
        return None

def reconnect_on_failure(func):
    """Decorator to handle reconnection if connection is lost."""
    def wrapper(cursor, con, query):
        attempts = 3  # Number of reconnection attempts
        delay = 5  # Delay between attempts in seconds

        for attempt in range(attempts):
            try:
                return func(cursor, con, query)
            except mysql.connector.errors.OperationalError as e:
                if e.errno == 2013:  # Error code for "Lost connection to MySQL server"
                    print(f"Connection lost on attempt {attempt + 1}, attempting to reconnect...")
                    con.close()  # Close the existing connection
                    time.sleep(delay)  # Wait before retrying
                    con = create_connection()  # Recreate the connection
                    cursor = con.cursor()  # Get a new cursor after reconnecting
                else:
                    raise e
        print("Reconnection attempts failed.")
        return None
    return wrapper

@reconnect_on_failure
def execute_query(cursor, con, query):
    """Executes a SQL query with automatic reconnection on failure."""
    cursor.execute(query)
    con.commit()

def set_database():
    con = create_connection()
    if con is None:
        print("Initial connection failed!")
        return None, None
    
    cursor = con.cursor()
    
    # SQL statements for creating tables
    create_db = "CREATE DATABASE IF NOT EXISTS stock_exp"
    
    create_table_stock_price = """
    CREATE TABLE IF NOT EXISTS stock_price (
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        stock_id INT NOT NULL,
        price INT NOT NULL
    );
    """
    
    create_company_data = """
    CREATE TABLE IF NOT EXISTS company_detail (
        comp_id INT PRIMARY KEY AUTO_INCREMENT,
        comp_name VARCHAR(100) UNIQUE,
        email VARCHAR(100) UNIQUE,
        phone_no VARCHAR(15),
        address VARCHAR(100),
        password VARCHAR(100)
    );
    """
    
    create_initial_stock_prices = """
    CREATE TABLE IF NOT EXISTS stock_initial (
        comp_id INT,
        initial_stock INT,
        stock_id INT,
        gross_expense INT,
        gross_income INT,
        stock_price INT,
        FOREIGN KEY (comp_id) REFERENCES company_detail(comp_id) ON DELETE CASCADE,
        PRIMARY KEY (stock_id)
    );
    """
    
    create_company_transaction_table = """
    CREATE TABLE IF NOT EXISTS company_transac (
        comp_transac_no INT PRIMARY KEY AUTO_INCREMENT,
        comp_id INT,
        stock_id INT,
        stock_quantity INT,
        transac_type VARCHAR(10),
        transac_quantity INT,
        Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
        price DECIMAL(20, 2),
        total_price DECIMAL(20, 2),
        FOREIGN KEY (comp_id) REFERENCES company_detail(comp_id),
        FOREIGN KEY (stock_id) REFERENCES stock_initial(stock_id)
    );
    """
    
    create_table_customer = """
    CREATE TABLE IF NOT EXISTS customer (
        cust_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,          
        phone VARCHAR(15),
        password VARCHAR(255) NOT NULL,
        age INT,
        gender VARCHAR(10)
    );
    """
    
    create_owned_stock = """
    CREATE TABLE IF NOT EXISTS owned_stock (
        cust_id INT,
        stock_name VARCHAR(100),
        stock_id INT,
        quantity INT,
        FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE CASCADE
    );
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
        total_price DECIMAL(20,2),
        FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE CASCADE,
        FOREIGN KEY (stock_id) REFERENCES stock_initial(stock_id) ON DELETE CASCADE
    );
    """
    
    # List of queries to execute
    queries = [
        create_db,
        "USE stock_exp",
        create_table_stock_price,
        create_company_data,
        create_initial_stock_prices,
        create_table_customer,
        create_owned_stock,
        create_customer_transac,
        create_company_transaction_table
    ]
    
    # Execute each query with reconnection handling
    for query in queries:
        execute_query(cursor, con, query)
    
    return cursor, con

if __name__ == "__main__":
    cursor, con = set_database()
    
    # Check if the connection was established and close it
    if con is not None and con.is_connected():
        con.close()
        print("The connection is closed.")
