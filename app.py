import os
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_toastr import Toastr
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["MONGO_DBNAME"] = 'private_media'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)
toastr = Toastr(app)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", 'error')
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "dob": request.form.get("dob").lower(),
            "address": request.form.get("address").lower(),
            "hobbies": request.form.get("hobbies").lower(),
            "events": request.form.get("events").lower()


        }
        mongo.db.users.insert_one(register)

        # Put new user into a session cookie
        session['user'] = request.form.get("username").lower()
        flash("Registration Successful!", 'success')
        return redirect(url_for("login", username=session["username"]))

    return render_template("register.html")



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
