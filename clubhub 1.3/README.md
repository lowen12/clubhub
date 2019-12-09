Project Overview:
Clubhub is a web application providing a consolidated place to find information about clubs on campus, because the
existing Hub does not contain complete information. It includes user-friendly features like search and filtering properties,
general club information, ratings and reviews, a Q&A page, and the ability for users to favorite and join clubs for
personalized experience.

Implementation:
Preliminary setup: Execute "cd clubhub", and "flask run"
Execution:
Upon opening the link, the user will be taken to the login page for ClubHub. ClubHub is only available to Harvard
affiliates; so the user can log in via their gmail by clicking on the “sign in” button on the top left corner and
is allowed access if their email address ends in “harvard.edu.”

Upon login, the user is directed to the homepage, which contains on the top a form to search or filter clubs; beneath
the form are the lists “My clubs,” “Favorites,” and “Clubs.” By default, “My clubs” and “Favorites” are empty, while
“Clubs” simply contains all clubs registered through the platform.

The main objective of ClubHub is to provide a more user-friendly and personalized experience than The Hub, Harvard’s
current repository of clubs. The user can either search by keywords contained in the club name (for those searching
for specific clubs) or filter clubs via multiple criteria (for those browsing clubs). The user is required to select
“Categories” from a list including but not confined to “All,” “Academic and Preprofessional,” “College Life,” “Creative
and Performing Arts,” “Media and Publications,” “Government and Politics,” etc., as well as “Comp Type” from a list of
“All,” “Application,” “Audition,” “Competition,” “Completion,” and “Interview.” The user can optionally input a range
(min, max) of time commitment (hours per week) and must input a minimum club rating. At the bottom of the form, the user
can click “Filter” button to filter for clubs, or “Clear Filter” to start again. Upon filtering, the “Clubs” list will
only display clubs that satisfy the desired features, instead of simply displaying all registered clubs.

Clicking on the name of a club brings the user to the “club” page. This page shows the user information about the club
that had been submitted via the “register” page. The user can click on the email, which is hyperlinked so as to prompt the email
app to open and autocomplete the "To" field with the address of the club. The website links to the external website of the club.
The page gives the user the ability to favorite the club and join the
club by clicking one of the buttons underneath the title, as well as reversing these actions via “unfavorite” and “unjoin.”
Upon these actions, the “Favorites” and “My Clubs” lists in the homepage will be populated. Users are able to ask questions
about the club via a form in the Q&A section. Users who have joined the club can submit answers to these questions. Users
who have joined the club are also able to click on “add a rating”, which brings them to another page where they can rate a club
(The rating page contains a form where users can specify the time committment of the club, give the club a rating between 1 and 5,
and write a review. New ratings and reviews will show up on the club's page). The sipmle average of existing ratings as well as
the number of ratings will be displayed. On the club's page, previous questions and answers and reviews can be accessed through
collapsible tables. If a question hasn't been answered, the answer field will contain a text input bar that allows members
to answer these questions.

In the navigation bar on the top-left corner, the user can return to the homepage, register for a new club, or log out.
“Register” takes the user to another html page, which features a form for which the user should input club name, description,
number of members, email, website, mailing address, month of officer election, of which the first two fields are required
and the rest optional. The registerer will additionally need to select all categories and “comp” types that apply to the
club, and evaluate the club via a rating on a 1-5 scale, a review, as well as an estimate for weekly time commitment.
“Log out” logs out the user, who will be taken back to the login page.

