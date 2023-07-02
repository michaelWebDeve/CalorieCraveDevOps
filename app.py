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
    recipes = Recipe.query.order_by(Recipe.id).limit(10).all()
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
                flash("Password incorrect!", "error")
        else:
            flash(email + " is not registered!", "error")
        return redirect(url_for("login"))
    else:
        if "email" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]
        conf_pwd = request.form["password_confirm"]

        exists = db.session.query(AppUser.id).filter_by(email=email).first() is not None
        if exists:
            flash("The email " + email + " is already registered!", "error")
        else:
            if pwd != conf_pwd:
                flash("Passwords are not matching", "error")
            else:
                session["email"] = email
                app_user = AppUser(email, pwd)
                db.session.add(app_user)
                db.session.commit()
                return redirect(url_for("user"))

    return render_template("register.html")


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
        flash("successfully logged out!", "success")
    else:
        flash("you were not logged in!", "error")
    return redirect(url_for("login"))


@app.route("/populate-db")
def pop_db():
    for i in range(35):
        base_image = open("static/images/base.jpg", "rb")
        total_kcal = 0
        total_protein = 0
        recipe = Recipe(name=f"Recipe{i}", description="Test description")
        ingredients = []
        ing_amount = random.randint(1, 10)
        for j in range(ing_amount):
            protein = random.randint(5, 30)
            carbs = random.randint(20, 60)
            fat = random.randint(5, 40)
            quantity = random.randint(50, 500)
            ing = RecipeIngredient(name=f"Ingredient{j}",
                                   protein=protein,
                                   quantity=quantity,
                                   carbs=carbs,
                                   fat=fat,
                                   recipe=recipe)

            total_kcal += ((protein*4.1) + (carbs*4.1) + (fat*9.3)) * (quantity/100)

            total_protein += protein * (quantity / 100)

            ingredients.append(ing)

        recipe.total_kcal = int(total_kcal)
        recipe.total_protein = int(total_protein)
        db.session.add(recipe)
        db.session.add_all(ingredients)
        db.session.commit()
        recipe_image = open(f"static/instance/images/{recipe.id}.jpg", "wb")
        for line in base_image:
            recipe_image.write(line)
        recipe_image.close()
        base_image.close()
    return "Database populated!"
