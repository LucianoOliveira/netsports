from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World! Welcome to NetSports! Uploaded from GitHub</p>"

@app.route("/test")
def test():
    return "<p>Testing New Route</p>"

@app.route("/new")
def new():
    return "<p>New Route from VsCode</p>"