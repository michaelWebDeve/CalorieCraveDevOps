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
    image_path = db.Column("image_path", db.String(200))

    ingredients = db.relationship('RecipeIngredient', backref='recipe')

    # def __init__(self, name, description, image_path):
    #     self.name = name
    #     self.description = description
    #     self.image_path = image_path
    def calc_kcal(self):
        total = 0
        for i in self.ingredients:
            total += i.kcal * (i.quantity / 100)
        return int(total)

    def get_img_path(self):
        return "instance/images/" + str(self.id) + ".jpg"


class RecipeIngredient(db.Model, SerializerMixin):
    __table_name__ = "recipe_ingredient"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    kcal = db.Column("kcal", db.Integer)
    protein = db.Column("protein", db.Integer)
    quantity = db.Column("quantity", db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    # def __init__(self, name, kcal, quantity):
    #     self.name = name
    #     self.kcal = kcal
    #     self.quantity = quantity
