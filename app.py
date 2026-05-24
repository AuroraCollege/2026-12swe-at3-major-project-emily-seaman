import json
import os
from flask import Flask, render_template

app = Flask(__name__)

DATA_DIR = "data"

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)

def save_json(filename, data):
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    recipes = load_json("recipes.json")
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)

#add recipe

@app.route("/add")
def add_page():
    return render_template("add_recipe.html")

from flask import request, redirect

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    recipes = load_json("recipes.json")

    ingredients_raw = request.form["ingredients"].split("\n")
    ingredients = [i.strip() for i in ingredients_raw if i.strip()]

    new_recipe = {
        "title": request.form["title"],
        "description": request.form["description"],
        "ingredients": ingredients
    }

    recipes.append(new_recipe)
    save_json("recipes.json", recipes)

    return redirect("/")

#pantry

@app.route("/pantry")
def pantry_page():
    pantry = load_json("pantry.json")
    return render_template("pantry.html", pantry=pantry)

from flask import request, redirect

@app.route("/add_pantry_item", methods=["POST"])
def add_pantry_item():
    pantry = load_json("pantry.json")
    new_item = request.form["item"]

    pantry.append(new_item)
    save_json("pantry.json", pantry)

    return redirect("/pantry")

# shopping list

@app.route("/shopping")
def shopping_page():
    shopping = load_json("shopping_list.json")
    return render_template("shopping.html", shopping=shopping)

@app.route("/add_to_shopping/<int:recipe_index>")
def add_to_shopping(recipe_index):
    recipes = load_json("recipes.json")
    pantry = [i.strip() for i in load_json("pantry.json")]
    shopping = [i.strip() for i in load_json("shopping_list.json")]

    recipe = recipes[recipe_index]
    ingredients = [i.strip() for i in recipe["ingredients"]]

    for item in ingredients:
        if item not in pantry and item not in shopping:
            shopping.append(item)

    save_json("shopping_list.json", shopping)

    return redirect("/shopping")

# backend route to generate the shopping list

@app.route("/add_to_shopping/<int:recipe_index>")
def add_to_shopping_route(recipe_index):
    recipes = load_json("recipes.json")
    pantry = [i.strip() for i in load_json("pantry.json")]
    shopping = [i.strip() for i in load_json("shopping_list.json")]

    recipe = recipes[recipe_index]
    ingredients = [i.strip() for i in recipe["ingredients"]]

    for item in ingredients:
        if item not in pantry and item not in shopping:
            shopping.append(item)

    save_json("shopping_list.json", shopping)

    return redirect("/shopping")

# complete recipe

@app.route("/complete_recipe/<int:index>")
def complete_recipe(index):
    recipes = load_json("recipes.json")
    recipe = recipes[index]
    return render_template("complete_recipe.html", recipe=recipe, index=index)

@app.route("/update_pantry_after_recipe/<int:index>", methods=["POST"])
def update_pantry_after_recipe(index):
    pantry = [i.strip() for i in load_json("pantry.json")]
    used_items = [i.strip() for i in request.form.getlist("used_items")]

    pantry = [item for item in pantry if item not in used_items]

    save_json("pantry.json", pantry)

    return redirect("/pantry")

@app.route("/got_item/<int:index>", methods=["POST"])
def got_item(index):
    shopping = load_json("shopping_list.json")

    if 0 <= index < len(shopping):
        shopping.pop(index)

    save_json("shopping_list.json", shopping)

    return redirect("/shopping")

