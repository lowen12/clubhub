function redirect(id) {
    // Check the club that was clicked
    document.getElementById(id).checked = true;

    // Submit the form
    document.getElementById("club_link").submit();
}

function onSignIn(googleUser) {
    // Set first name value
    document.getElementById("first_name").setAttribute("value", googleUser.getBasicProfile().getGivenName());

    // Submit the form
    document.getElementById("sign_in").submit();
}

// Retrieved from: https://developers.google.com/identity/sign-in/web/sign-in
function signOut() {
    // Sign out the user
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}