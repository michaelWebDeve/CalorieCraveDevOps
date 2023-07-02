from flask import Blueprint, request
from db import Recipe

api = Blueprint("api", __name__)


@api.route("/recipes/")
def fetch_recipes():

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

    if ("limit" and "counter") in request.args:
        limit = int(request.args.get("limit"))
        counter = int(request.args.get("counter"))
        recipes = recipes.paginate(page=counter, per_page=limit)

    res = []
    for r in recipes:
        res.append(r.to_dict(rules=("img_path", "ingredients_amount")))
    return res
