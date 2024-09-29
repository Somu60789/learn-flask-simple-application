from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome</h1>"

@app.route("/hello")
def hello():
    return "<h1>Hello World</h1>"

# URL processors 
@app.route("/greet/<name>")
def greet(name):
    return f"Hello {name}"

@app.route("/add/<int:number1>/<int:number2>")
def addition(number1, number2):
    return f"Sum of {number1} and {number2} is {number1 + number2}"

# Handelling url parameters
@app.route("/handle_url_parameters")
def handle_parms():
    if "greetings" in request.args.keys() and "name" in request.args.keys():
        greetings = request.args['greeting']
        name = request.args['name']
        return f"{greetings}, {name}"
    else:
        return "<h1>Some parameters are missing</h1>"

if __name__ == '__main__':
    app.run( host='0.0.0.0', port = 8080, debug = True)