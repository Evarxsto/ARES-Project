from flask import Flask, render_template,abort
import numpy as np
import matplotlib.colors

app = Flask(__name__)

board = None

# Variables
# Add the hue depending on confidence
# Change to hex codes
s_and_c = [("Focused","green"), ("Unfocused", "orange"), ("Drowsy", "lightblue")]

# Python Flask stuff
@app.route('/')
def index():
    """

    Renders the starter template where the color is white and there are no states associated
    with the 5 channels.
    """
    return render_template("dashboard.html", color="white", state="N/A", n=5)

@app.route('/update')
def update():

    # get all data from buffer

    # get band power values

    # return band power values
    colors = []
    for _ in range(5):
        rgb = np.random.random(3)
        colors.append(matplotlib.colors.to_hex(rgb))

    return {'data': colors}
