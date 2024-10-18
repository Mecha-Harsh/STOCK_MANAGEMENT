import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting

from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
import io
import random
import time

# rest of your code...


app = Flask(__name__)

def create_plot():
    # Generate sample data for the plot
    x = [i for i in range(10)]
    y = [random.randint(0, 10) for _ in range(10)]
    
    # Clear the plot and generate a new one
    plt.clf()
    plt.plot(x, y)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Dynamic Data Plot')

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plot_png():
    buf = create_plot()
    return Response(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
