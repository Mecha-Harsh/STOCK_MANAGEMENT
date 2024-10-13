import subprocess
import time

def run_programs():
    while True:
        # Start program1.py
        print("Running Program 1...")
        process1 = subprocess.Popen(['python', 'Stock-Management/Stock_update_2.py'])
        process1.wait() 
        # Start program2.py
        print("Running Program 2...")
        process2 = subprocess.Popen(['python', 'Stock-Management/examplegraph.py'])
        process2.wait()  # Wait for Program 2 to finish
        print("Waiting for 30 seconds...")
        time.sleep(10)

# Execute the function to run both programs
if __name__ == "__main__":
    try:
        run_programs()
    except KeyboardInterrupt:
        print("Terminating the program...")
