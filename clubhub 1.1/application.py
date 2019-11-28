import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clubhub.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show home page with filters"""

    # User submitted a filter
    if request.method == "POST":

        # Get all categories user selected
        categories = []
        all = False
        for checkbox in "all", "academic", "life", "arts", "culture", "gender", "government", "health", "hobbies", "media", "PBHA", "counseling", "service", "religion", "SEAS", "social", "women":
            value = request.form.get(checkbox)
            if value and checkbox == "all":
                all = True
            elif value and checkbox != "all":
                categories.append(checkbox)
            elif all == True:
                categories.append(checkbox)
        # Case where box checked
        if len(categories) != 0:
            while len(categories) < 16:
                categories.append(categories[-1])
        # Case where no box checked
        else:
            for checkbox in "academic", "life", "arts", "culture", "gender", "government", "health", "hobbies", "media", "PBHA", "counseling", "service", "religion", "SEAS", "social", "women":
                categories.append(checkbox)

        # Get all comp types user selected
        comps = []
        all = False
        for checkbox in "all", "application", "audition", "competition", "completion", "interview":
            value = request.form.get(checkbox)
            if value and checkbox == "all":
                all = True
            elif value and checkbox != "all":
                comps.append(checkbox)
            elif all == True:
                comps.append(checkbox)
        # Case where box checked
        if len(comps) != 0:
            while len(comps) < 5:
                comps.append(comps[-1])
        # Case where no box checked
        else:
            for checkbox in "application", "audition", "competition", "completion", "interview":
                comps.append(checkbox)

        # Get time commitement user selected
        if request.form.get("min"):
            min_time = int(request.form.get("min"))
        else:
            min_time = 0
        if request.form.get("max"):
            max_time = int(request.form.get("max"))
        else:
            max_time = 20

        # Ensure that minimum time is less than or equal to maximum time
        if min_time > max_time:
            return apology("invalid time range", 403)

        # Get ratings user selected
        if request.form["rating"]:
            rating = int(request.form["rating"])
        else:
            rating = 0

        # Get clubs matching filters from database
        clubs = db.execute("SELECT DISTINCT id, name FROM clubs WHERE id IN (SELECT club_id FROM categories WHERE category = ? OR category = ? OR "
                "category = ? OR category = ? OR category = ? OR category = ? OR category = ? OR category = ? OR category = ? OR "
                "category = ? OR category = ? OR category = ? OR category = ? OR category = ? OR category = ? OR category = ?) AND id IN (SELECT club_id FROM "
                "comps WHERE comp = ? OR comp = ? OR comp = ? OR comp = ? OR comp = ?) AND id IN (SELECT club_id FROM ratings WHERE (SELECT AVG(commitment) "
                "FROM ratings GROUP BY club_id) BETWEEN ? AND ?) AND id IN (SELECT club_id FROM ratings GROUP BY club_id HAVING AVG(rating) >= ?) ORDER BY name",
                categories[0], categories[1], categories[2], categories[3], categories[4], categories[5], categories[6], categories[7], categories[8],
                categories[9], categories[10], categories[11], categories[12], categories[13], categories[14], categories[15], comps[0],
                comps[1], comps[2], comps[3], comps[4], min_time, max_time, rating)

    else:
        # Get the names of all clubs
        clubs = db.execute("SELECT id, name FROM clubs ORDER BY name")

    # Get current user's first name
    first_name = db.execute("SELECT first FROM users WHERE id = ?",
            session["user_id"])

    # Get user's favorited clubs
    favorites = db.execute("SELECT id, name FROM clubs WHERE id IN (SELECT club_id FROM favorites WHERE user_id = ?) ORDER BY name",
            session["user_id"])

    return render_template("index.html", clubs = clubs, favorites = favorites, first_name = first_name[0]["first"])


@app.route("/club", methods=["GET", "POST"])
def club():
    """Display club description"""
    # Get club id
    club_id = request.form["club_id"]

    # Get information about selected club
    info = db.execute("SELECT * FROM clubs WHERE id = ?",
            int(club_id))

    # Set display value for favorite button
    favorite = db.execute("SELECT * FROM favorites WHERE user_id = ? AND club_id = ?",
                    int(session["user_id"]), int(club_id))
    if len(favorite) == 0:
        fav_status = "Add to Favorites"
    else:
        fav_status = "Remove from Favorites"

    # Favorite form was submitted
    if "favorite" in request.form:

        # Add club to favorites
        if fav_status == "Add to Favorites":
            db.execute("INSERT INTO favorites (user_id, club_id) VALUES (?, ?)",
                    int(session["user_id"]), int(club_id))
            fav_status = "Remove from Favorites"

        # Remove club from favorites
        else:
            db.execute("DELETE FROM favorites WHERE user_id = ? AND club_id = ?",
                    int(session["user_id"]), int(club_id))
            fav_status = "Add to Favorites"

    # Display page for the selected club
    return render_template("club.html", info = info[0], fav_status = fav_status)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User submitted the login form
    if request.method == "POST":

        # Add new users to the users table
        user_info = request.form;
        user = db.execute("SELECT * FROM users WHERE email = ?",
                user_info.get("email"))
        print(f"hi: {user}")

        if len(user) == 0:
            db.execute("INSERT INTO users (first, last, email, image) VALUES (?, ?, ?, ?)",
                    user_info.get("first_name"), user_info.get("last_name"), user_info.get("email"), user_info.get("image"))
            print("here")

        # Set the current user
        session["user_id"] = db.execute("SELECT id FROM users WHERE email = ?",
                user_info.get("email"))[0]["id"]

        # Display the home page
        return redirect("/")

    # User viewing the login page
    else:
        return render_template("login.html")


# Retrieved from Finance distribution code
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)