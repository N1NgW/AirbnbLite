from flask import Flask, Response, request, jsonify, redirect, render_template, \
                  url_for, make_response
from flask_pymongo import pymongo
from database import DatabaseConnection
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
db = DatabaseConnection()

@app.route("/addNewProperty", methods = ["GET", "POST"])
def addNewProperty():
    user = request.cookies.get("username") 
    if user == None:
        return render_template("invalid.html")
    if request.method == "GET":
        return render_template("addNewProperty.html")
    else:
        document = {
            "name": request.form["name"],
            "propertyType": request.form["type"],
            "price": request.form["price"],
            "owner": user,
            "renter": ""
        }
        db.insert("properties", document)
        return redirect(url_for("home"))

@app.route("/properties", methods = ["GET", "POST"])
def getProperties():
    user = request.cookies.get("username") 
    if user == None:
        return render_template("invalid.html")
    if request.method == "GET":
        properties = db.findMany("properties", {})
        return render_template("properties.html", properties = properties)
    else:
        id = request.form["button"] 
        db.update("properties", {"_id": ObjectId(id)}, {"$set": {"renter": user}})
        return redirect(url_for("getProperties"))
    
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
        return redirect("/login")

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
            resp = make_response(render_template("home.html"))
            resp.set_cookie("username", username)
            return resp
        else:
            return Response("incorrect password", status = 200, content_type = "text/html")    

@app.route("/logout", methods = ["GET"])
def logout():
    resp = make_response(render_template("login.html"))
    resp.set_cookie("username", "", expires = 0)
    return resp

@app.route("/home", methods = ["GET", "POST"])
def home():
    user = request.cookies.get("username") 
    if user == None:
        return render_template("invalid.html")
    if request.method == "GET":
        return render_template("home.html", greeting = greeting(user))
    else:
        if request.form["button"] == "I want to host":
            return redirect(url_for("addNewProperty"), code=303)
        else:
            return redirect(url_for("getProperties"), code=303)

@app.route("/account", methods = ["GET"])
def account():
    user = request.cookies.get("username") 
    if user == None:
        return render_template("invalid.html")
    properties = db.findMany("properties", {})
    return render_template("account.html", properties = properties, user = user)
    
@app.route("/removeProperty", methods = ["POST"])
def removeProperty():
    user = request.cookies.get("username")
    id = request.form["button"]
    db.deleteOne("properties", {"_id": ObjectId(id)})
    properties = db.findMany("properties", {})
    return render_template("account.html", properties = properties, user = user)

@app.route("/", methods = ["GET"])
def hello():
    return redirect(url_for("login"), code= 303)

def greeting(name):
    hourOfDay = datetime.datetime.now().time().hour
    greeting = ""
    if hourOfDay < 12:
        greeting = "Good morning "
    elif hourOfDay > 12 and hourOfDay < 18:
        greeting = "Good Afternoon "
    else:
        greeting = "Good Evening "
    greeting += name + "!"
    return greeting

if __name__ == "__main__":
    app.run(host = "localhost", port = 6000, debug = True)