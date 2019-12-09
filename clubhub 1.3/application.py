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

    # User submitted a filter or search
    if request.method == "POST":

        # User submitted the manual search form
        if "search" in request.form:

            # Find clubs with titles containing the user's search
            search = request.form.get("search")
            search1= '%' + search+ '%'
            clubs = db.execute("SELECT DISTINCT id, name FROM clubs WHERE name LIKE ?",
                    search1)

        # User submitted the check mark filter form
        else:

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
                    "comps WHERE comp = ? OR comp = ? OR comp = ? OR comp = ? OR comp = ?) AND id IN (SELECT club_id FROM ratings GROUP BY club_id HAVING AVG(commitment) "
                    "BETWEEN ? AND ?) AND id IN (SELECT club_id FROM ratings GROUP BY club_id HAVING AVG(rating) >= ?) ORDER BY name",
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

    # Get user's joined clubs
    joins = db.execute("SELECT id, name FROM clubs WHERE id IN (SELECT club_id FROM members WHERE user_id = ?) ORDER BY name",
            session["user_id"])

    return render_template("index.html", clubs = clubs, favorites = favorites, joins = joins, first_name = first_name[0]["first"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new club"""

    # User submitted the form to register a new club
    if request.method == "POST":

        # Check if the club already exists in the database
        exists = db.execute("SELECT * FROM clubs WHERE name = ?",
                request.form.get("club_name"))

        # Give an error if the club already exists
        if len(exists) != 0:
            return apology("A club with the same name already exists.", 403)

        # Add a new club to the database
        else:
            if len(request.form.get("members")) == 0:
                members = None
            else:
                members = request.form.get("members")
            if len(request.form.get("email")) == 0:
                email = None
            else:
                email = request.form.get("email")
            if len(request.form.get("website")) == 0:
                website = None
            else:
                website = request.form.get("website")
            if len(request.form.get("address")) == 0:
                address = None
            else:
                address = request.form.get("address")
            if len(request.form.get("elections")) == 0:
                elections = None
            else:
                elections = request.form.get("elections")
            if len(request.form.get("review")) == 0:
                review = None
            else:
                review = request.form.get("review")

            db.execute("INSERT INTO clubs (name, description, members, email, website, address, elections, commitment) VALUES (?, ?, ?, ?, ?, ?, ?, NULL)",
                    request.form.get("club_name"), request.form.get("description"), members, email, website, address, elections)

            # Add club's categories to the database
            club_id = db.execute("SELECT id FROM clubs WHERE name = ?",
                    request.form.get("club_name"))
            for checkbox in "academic", "life", "arts", "culture", "gender", "government", "health", "hobbies", "media", "PBHA", "counseling", "service", "religion", "SEAS", "social", "women":
                if request.form.get(checkbox):
                    db.execute("INSERT INTO categories (club_id, category) VALUES (?, ?)",
                           club_id[0]["id"] , checkbox)

            # Add club's comp types to the database
            for checkbox in "application", "audition", "competition", "completion", "interview":
                if request.form.get(checkbox):
                    db.execute("INSERT INTO comps (club_id, comp) VALUES (?, ?)",
                           club_id[0]["id"] , checkbox)

            # Add club's commitment and rating to the database
            db.execute("INSERT INTO ratings (club_id, rating, commitment, review) VALUES (?, ?, ?, ?)",
                    club_id[0]["id"], request.form.get("rating"), request.form.get("commitment"), review)

            return redirect("/")

    # User viewing the register page
    else:
        return render_template("register.html")


@app.route("/club", methods=["GET", "POST"])
def club():
    """Display club description"""

    # Get club id
    club_id = request.form["club_id"]

    # Rating form was submitted
    if "rating" in request.form:

        if len(request.form.get("review")) == 0:
            review = None
        else:
            review = request.form.get("review")

        # Check for duplicate reviews
        reviews = db.execute("SELECT * FROM ratings WHERE review = ?",
                request.form.get("review"))

        # Add rating to the database
        if len(reviews) == 0:
            db.execute("INSERT INTO ratings (club_id, rating, commitment, review) VALUES (?, ?, ?, ?)",
                    int(club_id), request.form.get("rating"), request.form.get("commitment"), review)

    # Question form was submitted
    if "question" in request.form:

        # Check for duplicate questions
        question = db.execute("SELECT * FROM questions WHERE question = ?",
                request.form.get("question"))

        # Add new questions to the database
        if len(question) == 0:
            db.execute("INSERT INTO questions (club_id, question, answer) VALUES (?, ?, NULL)",
                int(club_id), request.form.get("question"))

    # Answer form was submitted
    if "answer" in request.form:

        # Add club member's answer to the database
        db.execute("UPDATE questions SET answer = ? WHERE id = ?",
                    request.form.get("answer"), request.form.get("question_id"))

    # Get information about selected club
    info = db.execute("SELECT * FROM clubs WHERE id = ?",
            int(club_id))
    comps = db.execute("SELECT comp FROM comps WHERE club_id = ?",
            int(club_id))
    rating = db.execute("SELECT AVG(rating), AVG(commitment), COUNT(*) FROM ratings WHERE club_id = ?",
            int(club_id))
    review = db.execute("SELECT review FROM ratings WHERE club_id = ?",
            int(club_id))
    questions = db.execute("SELECT id, question, answer FROM questions WHERE club_id = ?",
            int(club_id))

    # Set display value for favorite button
    favorite = db.execute("SELECT * FROM favorites WHERE user_id = ? AND club_id = ?",
                    int(session["user_id"]), int(club_id))
    if len(favorite) == 0:
        fav_status = "Add to Favorites"
    else:
        fav_status = "Remove from Favorites"

    # Set display value for join button
    member = db.execute("SELECT * FROM members WHERE user_id = ? AND club_id = ?",
                    int(session["user_id"]), int(club_id))
    if len(member) == 0:
        member_status = "Join"
    else:
        member_status = "Unjoin"

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

    # Join form was submitted
    if "join" in request.form:

        # Add user to members
        if member_status == "Join":
            db.execute("INSERT INTO members (user_id, club_id) VALUES (?, ?)",
                    int(session["user_id"]), int(club_id))
            member_status = "Unjoin"

        # Remove user from members
        else:
            db.execute("DELETE FROM members WHERE user_id = ? AND club_id = ?",
                    int(session["user_id"]), int(club_id))
            member_status = "Join"

    # Display page for the selected club
    return render_template("club.html", info = info[0], comps = comps, rating = rating, review = review, questions = questions, fav_status = fav_status, member_status = member_status)


@app.route("/rate", methods=["GET", "POST"])
def rate():
    """Rate a club"""

    # Get club name
    info = db.execute("SELECT name, id FROM clubs WHERE id = ?",
            int(request.form.get("club_id1")))

    return render_template("rating.html", info = info)


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