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

        # Display the filtered results
        return render_template("index.html", clubs = clubs, first_name = session["user_id"])

    # Display the home page
    else:

        # Get the names of all clubs
        clubs = db.execute("SELECT id, name FROM clubs ORDER BY name")
        return render_template("index.html", clubs = clubs, first_name = session["user_id"])


@app.route("/club", methods=["GET", "POST"])
def club():
    """Display club description"""

    # Get information about selected club
    info = db.execute("SELECT * FROM clubs WHERE id = ?",
            int(request.form["club_id"]))

    # Display page for the selected club
    return render_template("club.html", info = info[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User submitted the login form
    if request.method == "POST":

        # Set the user
        session["user_id"] = request.form.get("first_name")

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