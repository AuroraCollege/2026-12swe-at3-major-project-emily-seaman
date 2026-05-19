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