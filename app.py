import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route('/home_page')
def home_page():
    return render_template("index.html")


@app.route("/")
@app.route("/get_recipes.meal")
def get_recipes_meal():
    recipes_meal = list(mongo.db.recipes.meal.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes=list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/")
@app.route("/add_recipe")
def add_recipe():
     return render_template("add_recipe.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        recipes = {
            "recipe_category": request.form.get("recipe_meal"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_time": request.form.get("recipe_time"),
            "recipe_serving": request.form.get("recipe_servings"),
        }
        mongo.db.tasks.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_recipes"))


    recipes = mongo.db.recipes.find().sort("recipes_name", 1)
    return render_template("add_task.html", recipes=recipes)
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)