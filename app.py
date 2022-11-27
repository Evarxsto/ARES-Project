from flask import Flask, render_template,abort
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Variables for Jinja
s_and_c = [("Focused","green"), ("Unfocused", "orange"), ("Drowsy", "lightblue")]

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("dashboard.html")

# Python Flask stuff
@app.route('/')
def index():
    state, color = s_and_c[2]
    return render_template("dashboard.html", color=color, state=state)
