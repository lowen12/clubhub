function goToClub(id) {
    // Check the club that was clicked
    document.getElementById(id).checked = true;

    // Submit the form
    document.getElementById("club_link").submit();
}

function checkRegister() {
    // Check for seleected categories
    var i = 7;
    var catSelected = false;
    while ((i < 23) && (catSelected === false)) {
        if (document.querySelectorAll("input")[i].checked === true) {
            catSelected = true;
        }
        i++;
    }
    // Check for selected comp types
    i = 23;
    var compSelected = false;
    while ((i < 28) && (compSelected === false)) {
        if (document.querySelectorAll("input")[i].checked === true) {
            compSelected = true;
        }
        i++;
    }

    // Ensure club name was inputted
    if (document.getElementById("club_name").value.length === 0) {
        document.getElementById("message").innerHTML = "Club name is required.";
    }
    // Ensure club description was inputted
    else if (document.getElementById("description").value.length === 0) {
        document.getElementById("message").innerHTML = "Club description is required.";
    }
    // Ensure category was selected
    else if (catSelected === false) {
        document.getElementById("message").innerHTML = "At least one category selection is required.";
    }
    // Ensure comp type was selected
    else if (compSelected === false) {
        document.getElementById("message").innerHTML = "At least one comp type selection is required.";
    }
    // Ensure time commitment was inputted
    else if (document.getElementById("commitment").value.length === 0) {
        document.getElementById("message").innerHTML = "Time commitment is required.";
    }
    // Ensure time commitment is a valid number
    else if ((document.getElementById("commitment").value < 1) || (document.getElementById("commitment").value > 20)) {
        document.getElementById("message").innerHTML = "Time commitment must be between 1 and 20.";
    }
    // Ensure rating was inputted
    else if (document.getElementById("rating").value.length === 0) {
        document.getElementById("message").innerHTML = "Rating is required.";
    }
    // Ensure rating is a valid number
    else if ((document.getElementById("rating").value < 1) || (document.getElementById("rating").value > 5)) {
        document.getElementById("message").innerHTML = "Rating must be between 1 and 5.";
    }
    // Submit complete forms
    else {
        document.getElementById("register").submit();
    }

}

function storeChecks() {
    // Remember search terms
    sessionStorage.setItem(0, document.querySelectorAll("input")[0].value);

    // Remember which filter boxes are checked in Category and Comp Type
    for (var i = 1; i < 24; i++) {
        if (document.querySelectorAll("input")[i].checked === true) {
            sessionStorage.setItem(i, 1);
        }
        else {
            sessionStorage.setItem(i, 0);
        }
    }

    // Remember the values in Time Commitment
    sessionStorage.setItem(24, document.querySelectorAll("input")[24].value);
    sessionStorage.setItem(25, document.querySelectorAll("input")[25].value);

    //Remember the checked box in rating
    for (var i = 26; i < 31; i++) {
        if (document.querySelectorAll("input")[i].checked === true) {
            sessionStorage.setItem(i, 1);
        }
        else {
            sessionStorage.setItem(i, 0);
        }
    }
}

function retrieveChecks() {
    // Only execute from index.html
    if (window.location.pathname === "/") {
        // Case where users has already submitted filter
        if (1 in sessionStorage) {
            // Set search term
            document.querySelectorAll("input")[0].value = sessionStorage.getItem(0);
            // Set checks for Category and Comp Type
            for (var i = 1; i < 24; i++) {
                if (sessionStorage.getItem(i) === "1") {
                    document.querySelectorAll("input")[i].checked = true;
                }
            }

            // Set values for Time Commitment
            document.querySelectorAll("input")[24].value = sessionStorage.getItem(24);
            document.querySelectorAll("input")[25].value = sessionStorage.getItem(25);

            // Set checks for Category and Comp Type
            for (var i = 26; i < 31; i++) {
                if (sessionStorage.getItem(i) === "1") {
                    document.querySelectorAll("input")[i].checked = true;
                }
            }
        }

        // Case where no filter applied yet
        else {
            sessionStorage.setItem(26, 1)
            for (var i = 27; i < 31; i++) {
                sessionStorage.setItem(i, 0);
            }
            document.querySelectorAll("input")[26].checked = true;
        }

        // Set all checks to unchecked and empty text in session storage
        sessionStorage.setItem(0, '');
        for (var i = 1; i < 24; i++) {
            sessionStorage.setItem(i, 0);
        }
        sessionStorage.setItem(24, null);
        sessionStorage.setItem(25, null);
    }
    // Executed from all pages not index.html
    else {
        // Clear filter values from storage when leaving index.html
        for (var i = 0; i < 31; i++) {
            sessionStorage.removeItem(i);
        }
    }
}

function clearFilter() {
    // Clear all filter information from memory
    for (var i = 1; i < 24; i++) {
        sessionStorage.setItem(i, 0);
    }
    sessionStorage.setItem(24, null);
    sessionStorage.setItem(25, null);
    sessionStorage.setItem(26, 1);
    for (var i = 27; i < 31; i++) {
        sessionStorage.setItem(i, 0);
    }
    document.querySelectorAll("input")[26].checked = true;
}

function onSignIn(googleUser) {
    // Set first name value
    document.getElementById("first_name").setAttribute("value", googleUser.getBasicProfile().getGivenName());
    document.getElementById("last_name").setAttribute("value", googleUser.getBasicProfile().getFamilyName());
    document.getElementById("email").setAttribute("value", googleUser.getBasicProfile().getEmail());
    document.getElementById("image").setAttribute("value", googleUser.getBasicProfile().getImageUrl());

    // Submit the form
    document.getElementById("sign_in").submit();
}

// Retrieved from: https://developers.google.com/identity/sign-in/web/sign-in
function signOut() {
    // clear session storage
    sessionStorage.clear();

    // Sign out the user
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}