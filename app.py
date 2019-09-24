from flask import Flask, Response, request, jsonify, redirect, render_template, url_for
from flask_pymongo import pymongo
from database import DatabaseConnection
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
db = DatabaseConnection()

@app.route("/addNewProperty", methods = ["GET", "POST"])
def addNewProperty():
    if request.method == "GET":
        return render_template("addNewProperty.html")
    else:
        document = {
            "name": request.form["name"],
            "propertyType": request.form["type"],
            "price": request.form["price"]
        }
        db.insert("properties", document)
        return redirect(url_for("home"), code = 303)

@app.route("/properties", methods = ["GET", "POST"])
def getProperties():
    if request.method == "GET":
        properties = db.findMany("properties", {})
        return render_template("properties.html", properties = properties)
    else:
        id = request.form["button"]
        print(id)
        rented = db.deleteOne("properties", {"_id": ObjectId(id)})
        print(rented)
        return redirect(url_for("getProperties"), code=303)
    
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        document = {
            "username": request.form["username"],
            "password": request.form["password"],
        }
        db.insert("user info", document)
        return redirect("/home", code=303)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        user = db.findOne("user info", {"username": username})
        if user == None:
            return Response("User doesn't exit", status = 200, content_type = "text/html")
        if password == user["password"]:
            return redirect(url_for("home", code = 303))
        else:
            return Response("incorrect password", status = 200, content_type = "text/html")    

@app.route("/home", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        if request.form["button"] == "I want to host":
            return redirect(url_for("addNewProperty"), code=303)
        else:
            return redirect(url_for("getProperties"), code=303)

@app.route("/", methods = ["GET"])
def hello():
    return redirect(url_for("login"), code= 303)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 6000, debug = True)