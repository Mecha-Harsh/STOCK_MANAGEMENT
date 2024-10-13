from createdatabase import set_database
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
import time

# Set up the database connection outside the loop
cursor, con = set_database()

# Set up the initial figure and formatting
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlabel("Time")
ax.set_ylabel("Stock Price")
ax.set_title("Live Stock Price - Last 10 Updates")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45, ha='right')

def fetch_and_update():
    # Fetch the latest data
    if cursor:
        cursor.execute("SELECT date_time, company FROM stock_price")
        value = cursor.fetchall()
        date = [row[0] for row in value]
        price = [row[1] for row in value]

        # Show only the last 10 updates
        date = date[-10:]
        price = price[-10:]

        # Clear the axes and plot the new data
        ax.clear()
        ax.plot(date, price, linestyle='-', marker='o', color='blue')
        
        # Update labels and format
        ax.set_xlabel("Time")
        ax.set_ylabel("Stock Price")
        ax.set_title("Live Stock Price - Last 10 Updates")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

# Set up the animation function to update every 30 seconds
ani = FuncAnimation(fig, lambda _: fetch_and_update())  # 30000 ms = 30 seconds

# Display the plot
plt.show()
