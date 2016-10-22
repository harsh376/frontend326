var gapi;
var app;
app.signIn = function() {
  // Get `GoogleAuth` instance
  var auth2 = gapi.auth2.getAuthInstance();

  // Sign-In
  auth2.signIn()
  .then(changeProfile);
};

/**
 * Trigger sign-out using Google Sign-In
 */
app.signOut = function() {
  // Get `GoogleAuth` instance
  var auth2 = gapi.auth2.getAuthInstance();

  // Sign-Out
  auth2.signOut()
  .then(changeProfile);
};

/**
 * Invoked when sign-in status is changed
 * @param  {GoogleUser} googleUser GoogleUser object obtained upon
 *                                 successful authentication
 */
var changeProfile = function(googleUser) {
  // See if `GoogleUser` object is obtained
  // If not, the user is signed out
  if (googleUser) {

    // Get `BasicProfile` object
    var profile = googleUser.getBasicProfile();

    // Get user's basic profile information
    app.profile = {
      name: profile.getName(),
      email: profile.getEmail(),
      imageUrl: profile.getImageUrl()
    };

    app.fire('show-toast', {
      text: "You're signed in."
    });

    app.$.dialog.close();

  } else {
    // Remove profile information
    // Polymer will take care of the rest
    app.profile = null;
    app.fire('show-toast', {
      text: "You're signed out."
    });
  }
};

// Initialization:
// Add `auth2` module
gapi.load('auth2', function() {
  // Initialize `auth2`
  gapi.auth2.init().then(function(auth2) {

    // If the user is already signed in
    if (auth2.isSignedIn.get()) {
      var googleUser = auth2.currentUser.get();

      // Change user's profile information
      changeProfile(googleUser);
    }
  });
});