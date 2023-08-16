import json
import os.path

from flask import Blueprint, request
from db import Recipe
from flask import Blueprint, request, jsonify, session
from db import Recipe, AppUser, db, FavouriteRecipe

api = Blueprint("api", __name__)
from app import app


@api.route("/recipes/", methods=["GET", "POST"])
def fetch_recipes():
    if request.method == "POST":
        recipe_data = json.loads(request.form.get("recipe"))
        recipe = Recipe(
            name=recipe_data["name"],
            description=recipe_data["description"],
            prep_time=int(recipe_data["prep_time"]),
            instruction=recipe_data["instruction"],
            vegetarian=recipe_data["vegetarian"],
            vegan=recipe_data["vegan"],
            gluten_free=recipe_data["gluten_free"]
        )
        recipe_image = request.files["recipeImage"]
        recipe_image.save(os.path.join(app.config["UPLOAD_FOLDER"], "test.jpg"))
        return "POSTED SUCCESSFULLY"
    else:
        recipes = Recipe.query.order_by(Recipe.id)
        if "min_kcal" in request.args:
            min_kcal = int(request.args.get("min_kcal"))
            recipes = recipes.filter(Recipe.total_kcal > min_kcal)

        if "max_kcal" in request.args:
            max_kcal = int(request.args.get("max_kcal"))
            recipes = recipes.filter(Recipe.total_kcal < max_kcal)

        if "min_protein" in request.args:
            min_protein = int(request.args.get("min_protein"))
            recipes = recipes.filter(Recipe.total_protein > min_protein)

        if "max_prep_time" in request.args:
            max_prep_time = int(request.args.get("max_prep_time"))
            recipes = recipes.filter(Recipe.prep_time < max_prep_time)

        if "vegan" in request.args:
            recipes = recipes.filter(Recipe.vegan)

        if "vegetarian" in request.args:
            recipes = recipes.filter(Recipe.vegetarian)

        if "gluten_free" in request.args:
            recipes = recipes.filter(Recipe.gluten_free)

        if "favorites_only" in request.args:
            user_id = request.args.get("user_id")
            favorite_recipes = FavouriteRecipe.query.filter_by(user_id=user_id).all()
            if favorite_recipes:
                favorite_recipe_ids = [fav.recipe_id for fav in favorite_recipes]
                recipes = recipes.filter(Recipe.id.in_(favorite_recipe_ids))

        if ("limit" and "counter") in request.args:
            limit = int(request.args.get("limit"))
            counter = int(request.args.get("counter"))
            recipes = recipes.paginate(page=counter, per_page=limit)

    res = []
    for r in recipes:
        res_dict = r.to_dict(rules=("img_path", "ingredients_amount"))
        if "user_id" in request.args:
            res_dict["favorite"] = r.is_favorite(request.args["user_id"])
        res.append(res_dict)
    return res


@api.route("/toggle_favorite", methods=["POST"])
def add_to_favourites():
    args = request.args
    if "user_id" and "recipe_id" in args:
        user_id = int(request.args.get("user_id"))
        recipe_id = int(request.args.get("recipe_id"))
        existing_favourite = FavouriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        if not existing_favourite:
            new_favourite = FavouriteRecipe(user_id=user_id, recipe_id=recipe_id)
            db.session.add(new_favourite)
            db.session.commit()
            return "on"
        else:
            db.session.delete(existing_favourite)
            db.session.commit()
            return "off"
    return "non"



