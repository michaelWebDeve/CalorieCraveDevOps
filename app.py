
import os
import random

from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/instance/images/"

from db import AppUser
from db import db
from db import Recipe, RecipeIngredient
from api import api

app.register_blueprint(api, url_prefix="/api")


@app.route('/')
def index():
    if "email" in session:
        return render_template("home.html")
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
                session["user_id"] = app_user.id
                return redirect(url_for("index"))
            else:
                flash("Password incorrect!", "error")
        else:
            flash(email + " is not registered!", "error")
        return redirect(url_for("login"))
    else:
        if "email" in session:
            return redirect(url_for("index"))
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
                session["user_id"] = app_user.id
                return redirect(url_for("index"))

    return render_template("register.html")


@app.route('/user')
def user():
    if "email" in session:
        email = session["email"]
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))


@app.route('/change_email', methods=["POST"])
def change_email():
    if "email" not in session:
        flash("You are not logged in!", "error")
        return redirect(url_for("login"))

    new_email = request.form["newEmail"]
    current_password = request.form["currentPasswordChangeEmail"]

    app_user = db.session.query(AppUser).filter_by(email=session["email"]).first()
    if app_user is None or app_user.pwd != current_password:
        flash("Current password incorrect!", "error")
        return redirect(url_for("user"))

    app_user.email = new_email
    db.session.commit()
    session["email"] = new_email

    flash("Email changed successfully!", "success")
    return redirect(url_for("user"))


@app.route('/change_password', methods=["POST"])
def change_password():
    if "email" not in session:
        flash("You are not logged in!", "error")
        return redirect(url_for("login"))

    current_password = request.form["currentPassword"]
    new_password = request.form["newPassword"]
    confirm_password = request.form["newPassword2"]

    if new_password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect(url_for("user"))

    app_user = db.session.query(AppUser).filter_by(email=session["email"]).first()
    if app_user is None or app_user.pwd != current_password:
        flash("Current password incorrect!", "error")
        return redirect(url_for("user"))

    app_user.pwd = new_password
    db.session.commit()

    flash("Password changed successfully!", "success")
    return redirect(url_for("user"))


@app.route('/logout')
def logout():
    if "email" in session:
        session.clear()
        flash("successfully logged out!", "success")
    else:
        flash("you were not logged in!", "error")
    return redirect(url_for("login"))


@app.route("/recipe/<recipe_id>")
def get_recipe(recipe_id):
    recipe_id = int(recipe_id)
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return render_template("recipe.html", r=recipe)
    else:
        return "404"


@app.route("/populate-db")
def pop_db():
    if os.path.exists("./static/instance"):
        print("exists")
        if os.path.exists("./static/instance/images"):
            print("exists")
        else:
            os.mkdir("./static/instance/images")
    else:
        os.mkdir("./static/instance")
        os.mkdir("./static/instance/images")

    for i in range(35):
        base_image = open("static/images/base.jpg", "rb")
        total_kcal = 0
        total_protein = 0
        prep_time = random.randint(5, 120)
        description = "Demo description"
        instruction = """
        1. Erste Anweisung 
        2. Zweite Anweisung
        3. Dritte Anweisung
        """
        vegetarian = bool(random.randint(0, 1))
        vegan = bool(random.randint(0, 1))
        gluten_free = bool(random.randint(0, 1))
        recipe = Recipe(name=f"Recipe{i}", description=description, instruction=instruction, prep_time=prep_time)
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

            total_kcal += ((protein * 4.1) + (carbs * 4.1) + (fat * 9.3)) * (quantity / 100)

            total_protein += protein * (quantity / 100)

            ingredients.append(ing)

        recipe.vegan = vegan
        recipe.vegetarian = vegetarian
        recipe.gluten_free = gluten_free
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


@app.route("/create-recipe")
def create_recipe():
    return render_template("create_recipe.html")



@app.before_request
def create_database():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
