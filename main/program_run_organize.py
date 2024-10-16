import subprocess
import time

# Start the first process with an infinite loop
process1 = subprocess.Popen(['python', 'main\\Stockpriceupdate.py'])

# Start the second process without waiting for the first process to complete
str = r"main\register_companya.py"
process2 = subprocess.Popen(['python', str])
