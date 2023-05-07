import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class AppUser(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    pwd = db.Column("pwd", db.String(100))

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd


@app.route('/')
def index():
    db.create_all()
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["emailAdr"]
        pw = request.form["pwd"]

        app_user = db.session.query(AppUser).filter_by(email=email).first()
        if app_user is not None:
            if app_user.pwd == pw:
                session["email"] = email
                return redirect(url_for("user"))
            else:
                flash("Password incorrect!")
        else:
            flash(email + " is not registered!")
        return redirect(url_for("login"))
    else:
        if "email" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")


@app.route('/user')
def user():
    if "email" in session:
        email = session["email"]
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        flash("successfully logged out!")
    else:
        flash("you were not logged in!")
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["emailAdr"]
        pwd = request.form["pwd"]
        conf_pwd = request.form["confPwd"]

        exists = db.session.query(AppUser.id).filter_by(email=email).first() is not None
        if exists:
            flash("The email " + email + " is already registered!")
        else:
            if pwd != conf_pwd:
                flash("Passwords are not matching")
            else:
                session["email"] = email
                app_user = AppUser(email, pwd)
                db.session.add(app_user)
                db.session.commit()
                return redirect(url_for("user"))

    return render_template("register.html")
