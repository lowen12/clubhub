function goToClub(id) {
    // Check the club that was clicked
    document.getElementById(id).checked = true;

    // Submit the form
    document.getElementById("club_link").submit();
}

function storeChecks() {
    // Remember which filter boxes are checked in Category and Comp Type
    for (var i = 0; i < 23; i++) {
        if (document.querySelectorAll("input")[i].checked === true) {
            sessionStorage.setItem(i, 1);
        }
        else {
            sessionStorage.setItem(i, 0);
        }
    }

    // Remember the values in Time Commitment
    sessionStorage.setItem(23, document.querySelectorAll("input")[23].value);
    sessionStorage.setItem(24, document.querySelectorAll("input")[24].value);

    //Remember the checked box in rating
    for (var i = 25; i < 30; i++) {
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
            // Set checks for Category and Comp Type
            for (var i = 0; i < 23; i++) {
                if (sessionStorage.getItem(i) === "1") {
                    document.querySelectorAll("input")[i].checked = true;
                }
            }

            // Set values for Time Commitment
            document.querySelectorAll("input")[23].value = sessionStorage.getItem(23);
            document.querySelectorAll("input")[24].value = sessionStorage.getItem(24);

            // Set checks for Category and Comp Type
            for (var i = 25; i < 30; i++) {
                if (sessionStorage.getItem(i) === "1") {
                    document.querySelectorAll("input")[i].checked = true;
                }
            }
        }

        // Case where no filter applied yet
        else {
            sessionStorage.setItem(25, 1)
            for (var i = 26; i < 30; i++) {
                sessionStorage.setItem(i, 0);
            }
            document.querySelectorAll("input")[25].checked = true;
        }

        // Set all checks to unchecked and empty text in session storage
        for (var i = 0; i < 23; i++) {
            sessionStorage.setItem(i, 0);
        }
        sessionStorage.setItem(23, null);
        sessionStorage.setItem(24, null);
    }
    // Executed from all pages not index.html
    else {
        // Clear filter values from storage when leaving index.html
        for (var i = 0; i < 30; i++) {
            sessionStorage.removeItem(i);
        }
    }
}

function clearFilter() {
    // Clear all filter information from memory
    for (var i = 0; i < 23; i++) {
        sessionStorage.setItem(i, 0);
    }
    sessionStorage.setItem(23, null);
    sessionStorage.setItem(24, null);
    sessionStorage.setItem(25, 1)
    for (var i = 26; i < 30; i++) {
        sessionStorage.setItem(i, 0);
    }
    document.querySelectorAll("input")[25].checked = true;
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