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
    created_by = db.Column(db.Integer, db.ForeignKey("app_user.id"))  # fk aus user Tabelle
    name = db.Column("name", db.String(100))
    description = db.Column("description", db.Text)
    instruction = db.Column("instruction", db.Text)
    prep_time = db.Column("prep_time", db.Integer)
    total_kcal = db.Column("total_kcal", db.Integer)
    total_protein = db.Column("total_protein", db.Integer)
    vegetarian = db.Column("vegetarian", db.Boolean)
    vegan = db.Column("vegan", db.Boolean)
    gluten_free = db.Column("gluten_free", db.Boolean)

    ingredients = db.relationship('RecipeIngredient', backref='recipe')

    def img_path(self):
        return "instance/images/" + str(self.id) + ".jpg"

    def ingredients_amount(self):
        return len(self.ingredients)

    def instruction_list(self):
        return self.instruction.split("\n")


class RecipeIngredient(db.Model, SerializerMixin):
    __table_name__ = "recipe_ingredient"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    fat = db.Column("fat", db.Integer)
    carbs = db.Column("carbs", db.Integer)
    protein = db.Column("protein", db.Integer)
    quantity = db.Column("quantity", db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))


class FavouriteRecipe(db.Model, SerializerMixin):
    __table_name__ = "favourite_recipes"
    # fk zusammensetzen zu einer pk
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)

    user = db.relationship("AppUser", backref="favourite_recipes")  # new column "favourite_recipes" on child(AppUser)
    recipe = db.relationship("Recipe")  # Beziehung zwischen favourite_recipe und Recipe tabelle

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id
# ermöglicht initialisierung der fk



