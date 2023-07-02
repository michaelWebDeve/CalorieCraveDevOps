from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

from app import app

db = SQLAlchemy(app)


class AppUser(db.Model):
    __table_name__ = "app_user"

    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    pwd = db.Column("pwd", db.String(100))

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd


class Recipe(db.Model, SerializerMixin):
    __table_name__ = "recipe"

    serialize_rules = ("-ingredients.recipe",)

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    description = db.Column("description", db.String(100))
    prep_time = db.Column("prep_time", db.Integer)
    total_kcal = db.Column("total_kcal", db.Integer)
    total_protein = db.Column("total_protein", db.Integer)

    ingredients = db.relationship('RecipeIngredient', backref='recipe')

    def img_path(self):
        return "instance/images/" + str(self.id) + ".jpg"

    def ingredients_amount(self):
        return len(self.ingredients)


class RecipeIngredient(db.Model, SerializerMixin):
    __table_name__ = "recipe_ingredient"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    fat = db.Column("fat", db.Integer)
    carbs = db.Column("carbs", db.Integer)
    protein = db.Column("protein", db.Integer)
    quantity = db.Column("quantity", db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
