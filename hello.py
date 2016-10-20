# a sample flask app

from flask import Flask
app = Flask(__name__)

#@app.route() declares
#url for which this happens
@app.route('/')
def hello_world():
    return 'Hello, World!'

