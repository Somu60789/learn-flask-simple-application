from flask import Flask, request, make_response, render_template, redirect, url_for, Response, send_from_directory, jsonify, session
import pandas as pd
import os, uuid

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
app.secret_key = "2405:201:c058:a842:8f6e:1687:4c25:d632"

@app.route('/')
def index():
    return "<h1>Welcome</h1>"

# Usage of port numbers
@app.route("/hello")
def hello():
    return "<h1>Hello World</h1>", 200

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
    

# Handelling api method callings 

# GET    -- to get something
# POST   -- to create something
# PUT    -- to update something
# DELETE -- to delete something

# Function can able to allow the methods which ever present in the list else default GET

@app.route("/api-methods", methods = ["GET", "PUT", "POST", "DELETE"])
def api_method_handelling():
    if request.method == "GET":
        return "You called GET method\n"
    elif request.method == "PUT":
        return "You called PUT method\n"
    elif request.method == "POST":
        return "You called POST method\n"
    elif request.method == "DELETE":
        return "You called DELETE method\n"
    else:
        return "You will never ever come here"
    
# custome response
@app.route("/custom-response")
def custom_response():
    response = make_response("We modified headers \n")
    response.status_code = 202
    response.headers["content-type"] = "application/json"
    return response


# Template usage
@app.route("/give-hello-world-template")
def give_hello_world():
    name = "Somasekhar"
    lname = "Eruvuri"
    list = ["somu", "ramu", "mamu"]
    return render_template("hello.html", name=name, lname=lname, list=list, message = "Hello")

# Use a template each time we need html page instead of creating every time
@app.route("/template-inheretence")
def template_page():
    name = "Somasekhar"
    lname = "Eruvuri"
    list = ["somu", "ramu", "mamu"]
    return render_template("other.html", name=name, lname=lname, list=list)

# Usage of filters
@app.route("/filter")
def filter():
    name = "Somasekhar"
    lname = "Eruvuri"
    list = ["somu", "ramu", "mamu"]
    return render_template("filters.html", name=name, lname=lname, list=list)

@app.template_filter("reverse")
def reverse(s):
    return s[::-1]

@app.template_filter("repeat")
def repeat(s, n=2):
    return s*n

# Redirection
@app.route("/redirect")
def redirection():
    return redirect(url_for("hello"))


# Handelling POST request and FOrms
@app.route("/dummy-login", methods = ["GET", "POST"])
def dummyLogin():
    if request.method == "GET":
        return render_template("dummyLogin.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return "Success Login" if (username == "Somu60789" and password == "Nlrdpa@1998") else "Failure Login"

@app.route("/file-upload", methods = ["POST"])
def fileUpload():
    file = request.files["file"]
    if file.content_type == "text/plain":
        return file.read().decode()
    return "Done"    


@app.route("/convert-csv", methods = ["POST"])
def convertCSV():
    file = request.files["file"]
    df = pd.read_excel(file)
    response = Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename = result.csv"
        }
    )
    return response

@app.route("/convert-csv-2", methods = ["POST"])
def convertCSV2():
    file = request.files["file"]
    df = pd.read_excel(file)
    if not os.path.exists("downloads-flask-app"):
        os.mkdir("downloads-flask-app")
    fileName = f"{uuid.uuid4()}.csv"
    df.to_csv(os.path.join("downloads-flask-app", fileName))

    return render_template("download.html", fileName=fileName)

@app.route("/downloads")
def download():
    fileName = request.args.get("filename")
    return send_from_directory("downloads-flask-app", fileName, download_name = "result.csv")


@app.route("/handle-post", methods = ["POST"])
def handlePost():
    greeting = request.json["greeting"]
    name = request.json["name"]
    with open("file.txt", "w") as f:
        f.write(f"{greeting}, {name}")
    return jsonify({"message": "Successfully written!"})

@app.route("/set-data")
def setData():
    session["name"] = "Somasekhar"
    session["other"] = "Hello World"
    return render_template("hello.html", message = "Session data set!!!")

@app.route("/get-data")
def getData():
    if "name" in session.keys() and "other" in session.keys():
        name = session["name"]
        other = session["other"]
        return render_template("hello.html", message = f"Name: {name}, Other: {other}")
    else:
        return render_template("hello.html", message = f"No session data has been set !!")


if __name__ == '__main__':
    app.run( host='0.0.0.0', port = 8080, debug = True)