from flask import Flask, render_template,abort

app = Flask(__name__)

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
