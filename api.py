from flask import Blueprint, request
from db import Recipe

api = Blueprint("api", __name__)


@api.route("/recipes/")
def fetch_recipes():
    counter = int(request.args.get("counter"))
    limit = int(request.args.get("limit"))
    res = []
    recipes = Recipe.query.order_by(Recipe.id).paginate(page=counter, per_page=limit)
    for r in recipes:
        res.append(r.to_dict(rules=("img_path", "total_kcal", "ingredients_amount", "total_protein")))
    return res

