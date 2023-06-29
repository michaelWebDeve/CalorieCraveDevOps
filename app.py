import os
import random
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import AppUser
from db import db
from db import Recipe, RecipeIngredient
from api import api

app.register_blueprint(api, url_prefix="/api")


@app.route('/')
def index():
    db.create_all()
    recipes = Recipe.query.all()
    if "email" in session:
        return render_template("home.html", recipes=recipes)
    return redirect(url_for("login"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pw = request.form["password"]

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
        email = request.form["email"]
        pwd = request.form["password"]
        conf_pwd = request.form["password_confirm"]

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


@app.route("/populate-db")
def pop_db():

    for i in range(20):
        base_image = open("static/images/base.jpg", "rb")
        recipe = Recipe(name=f"Recipe{i}", description="Test description")
        ingredients = []
        ing_amount = random.randint(1, 10)
        for j in range(ing_amount):
            kcal = random.randint(0, 500)
            quantity = random.randint(50, 500)
            ing = RecipeIngredient(name=f"Ingredient{j}", kcal=kcal, quantity=quantity, recipe=recipe)
            ingredients.append(ing)

        db.session.add(recipe)
        db.session.add_all(ingredients)
        db.session.commit()
        recipe_image = open(f"static/instance/images/{recipe.id}.jpg", "wb")
        for line in base_image:
            recipe_image.write(line)
        recipe_image.close()
        base_image.close()
    return "Database populated!"
