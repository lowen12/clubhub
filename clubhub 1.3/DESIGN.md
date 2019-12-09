The ClubHub login page has an Google login icon which initiates a popup for users to sign in via a Google email account when clicked. The Google
login settings for ClubHub are configured in such a way that only users whose email addresses end in harvard.edu can gain access. Once users enter
a valid Harvard email and password, the user's id is stored in "application.py" and the user is redirected to the home page. Google login provides
a secure login method analogous to HarvardKey login.

The home page includes a keyword search, filtering by checking boxes and inputting text, and lists of clubs separated into "My Clubs,"
"Favorites," and "Clubs." The keyword search works through a form in "index.html" that allows users to search clubs by words in their names. When
submitted, the form provides values to "\" in "application.py" where the program calls a SQL query to select clubs whose names include the searched
words. The selected clubs are then displayed under "Clubs" in "index.html". Filtering also utilizes a form to collect the boxes that users check
for "categories," "comp types," and "rating," and values they input in "time commitment". In the same way as the search form, the filtering form
passes users' inputs to "\" in "application.py". The python code calls a SQL query selecting all clubs fitting the chosen values and displays their
names under "Clubs" in "index.html". Both the submit button for the search form and the filtering form include references to a javascript function
that stores users' inputted values in session memory. Another javascript function that runs each time "index.html" loads displays thsose stored
values. These javascript functions allow users' inputs to remain visible even after the "index.html" is refreshed to display search or filter
results. Saving the inputs improves user experience by helping users remember what they searched or filtered for. The listings under "My
Clubs" shows clubs that a particular user has joined, which are saved in a database table linking user IDs with the IDs of clubs they have joined.
"Favorites" displays clubs the user has favorited, saved similarly to joined clubs in another table linking user IDs with the IDs of clubs they
have favorited. Joining and favoriting clubs is possible through "club.html". "Clubs" gives a listing of all clubs existing in the database.
Creating separate lists for joined and favorited clubs allows users to more quickly access the clubs whose websites they frequent.

The homepage also contains the Navigation bar, which consists of hyperlinked tabs to "Home," "Register," and "Log Out." Since it is contained in the "layout.html" page, it will be displayed on all webpages of ClubHub once
the user logs in. From the home page, users are redirected to clubs' individual pages when they click on listed club names. Clicking on a club's name submits a hidden
form passing the clicked club's id in the database to "/club" in "application.py". Taking the club's id, the python program makes a SQL query to
select information stored about that particular club. Next, it displays "club.html" customized with the club's information. If statements in
"club.html" ensure that only information available about the club is displayed. Furthermore, the clubs' websites are linked to the actual website
URL in "club.html" and clicking the clubs' email addresses opens a new email addressed to the club in the mail app installed on the user's laptop.
The club page has buttons to join or favorite clubs, submit questions in the Q&A section, and answer Q&A questions if they are members of the club.
Clicking the join button submits a form with hidden inputs, an input identifying the submitted form as the join form and an input with the current
club's ID in the database. "/club" in "application.py" executes an if statement when the join form is submitted to add the user's ID and the
club's ID to the members table in the database. It also changes the lable on the join button to "Unjoin" from "Join". Clicking "Unjoin" deletes
the database entry linking the users and the club. The favorite button performs the same function as the join button, but adds users and clubs to
the favorites table in the database. Once a user has favorited a club, the favorite button changes to "Unfavorite" from "Favorite" due to passing
a variable with a different value from "application.py" to "club.html". Clicking the button to submit a question to the Q&A submits a form with
the user's question. "/club" in "application.py" receives the question and inserts it into the questions table of the database along with
the club's ID where the question was submitted. The question is only added to the database if it is not a duplicate to prevent duplicate questions,
particularly when the club page is refreshed after submitting a question. Questions are displayed on the club page through a for loop in "club.html"
that also shows an answer input box if the users has joined to club and "Unanswered" if the user has not joined the club. Only displaying the
answer box to club members prevents nonmembers from incorrectly answering questions. When the answer button is clicked, the answer is added to the
question table in the database via "/club" in "application.py" and a javascript function hides the answer box so each question can only have one
answer. Previous questions and answers and reviews are inside dropdown bars controlled with javascript functions for easier user access.

Once users have joined a club, they can access a link to create a rating for the club. Clicking on the link redirects users to "rating.html". This
page contains a form to submit a rating, time commitment, and review for the club. When the submit button is clicked, an javascript function runs
to ensure that the required inputs of rating and time commitment are completed before submission. If either of those fields are empty, the
javascript produces a warning in "rating.html". After the form is successfully submitted, the users' rating is stored in the ratings table in the
database and the average rating, average time commitment, and reveiws for that club are updated on refresh.

From the homepage, users can access the register page from the menu. The register page includes a form that allows users to input a new club and its
information (including name, description, number of members, email, website, mailing address, month of officer elections, time commitment, rating,
and reviews). Users also select a checkbox to specify the club's category and comp type. All of this information is submitted to the database via
insert statements written in SQL. A user cannot enter the name of a club that already exists because the variable "exists" in python selects all the
club_name rows, and if the new club matches a name in exists, an apology is returned. All of the code to check if user input is valid lives in clubhub.js.
The function checkRegister checks to make sure the user fills out all necessary information. To make sure a club name is entered, we check if the length
of the value in getElementById("club_name") is 0, and if it is the user is prompted to enter a club name. The same is done for club description, time
committment, and rating. We also check if the values input into time commitment and rating are valid (time committment must be between 1 and 20, and rating
must be between 1 and 5). All of the warning messages appear next to the "register club" button. If a user neglects to input information for the required
fields, the javascript will return an error message and prompt the user to complete said field.
If all input is valid, the newe club will be added to the database upon clicking "register club."

The database clubhub.db contains the relevant databases to organize club and user information. The "clubs" table contains the fields id, name,
description, members, email, website, address, elections, and commitment, where id is the primary key and unique identification for clubs. Similarly,
the "users" table contains id, first, last, email, image. The "categories" and "comps" tables specify the respective feature for each club. Note that
a club can simultaneously fall under multiple categories and/or have multiple comp processes. The "ratings" table aggregates all ratings, reviews, and
time commitments for clubs; the "questions" table keeps track of submitted questions and answer. The "favorites" and "members" tables links the clubs
table with the user table, and connect both via club id and user id.

The logout segment in "application.py" clears the session by forgetting the current user id and redirects the user to the login page.

"apology.html" renders errors. For instance, if a user tries to register a club whose name already exists in the database, the user is redirected to
"apology.html" which displays a complaint.

The style code is contained in styles.css. The background images for each page are in the following css files (clubstyle.css, indesxstyle.css,
ratingstyle.css, and registerstyle.css). In styles.css we formatted all of the divisions and set the position for all of the elements. We also
styled the sidebar, the buttons, and the input forms.


