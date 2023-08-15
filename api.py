from flask import Blueprint, request, jsonify, session
from db import Recipe, AppUser, db, FavouriteRecipe

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

    if "vegan" in request.args:
        recipes = recipes.filter(Recipe.vegan)

    if "vegetarian" in request.args:
        recipes = recipes.filter(Recipe.vegetarian)

    if "gluten_free" in request.args:
        recipes = recipes.filter(Recipe.gluten_free)

    if ("limit" and "counter") in request.args:
        limit = int(request.args.get("limit"))
        counter = int(request.args.get("counter"))
        recipes = recipes.paginate(page=counter, per_page=limit)

    if "favorites" in request.args:
        if "email" in session:
            email = session["email"]

            # user id aus der usertabelle
            user = db.session.query(AppUser).filter_by(email=email).first()

            if user:
                # aus FavoriteRecipe Tabelle fav meal abfragen können
                favorite_recipes = db.session.query(FavouriteRecipe).filter_by(user_id=user.id).all()

                if favorite_recipes:
                    favorite_recipe_ids = [fav.recipe_id for fav in favorite_recipes]
                    recipes = db.session.query(Recipe).filter(Recipe.id.in_(favorite_recipe_ids)).all()
                    # mit den fav_recipe_ids das Rezept aud der Recipe Tabelle holen
                else:
                    return jsonify([])  # keine favs leere Liste
            else:
                return jsonify([])  # user nt gefunden leere liste

    res = []
    for r in recipes:
        res.append(r.to_dict(rules=("img_path", "ingredients_amount")))
    return res


@api.route("/add_to_favourites", methods=["POST"])
def add_to_favourites():
    if "email" in session:
        email = session["email"]
        user = db.session.query(AppUser).filter_by(email=email).first()

        if user:
            recipe_id = request.form.get("recipe_id")
            existing_favourite = FavouriteRecipe.query.filter_by(user_id=user.id, recipe_id=recipe_id).first()

            if not existing_favourite:
                new_favourite = FavouriteRecipe(user_id=user.id, recipe_id=recipe_id)
                db.session.add(new_favourite)
                db.session.commit()
                return jsonify(success=True)

    return jsonify(success=False)



