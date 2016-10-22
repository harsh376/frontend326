<html>
  <head>
    <title>Search Engine</title>
    <link type="text/css" href="static/css/home.css" rel="stylesheet">
    <meta name="google-signin-scope" content="profile email">
    <meta name="google-signin-client_id" content="693905804431-emi5shf5mskr1iu5aetihih32o19q4mv.apps.googleusercontent.com">
    <script src="https://apis.google.com/js/platform.js" async defer></script>
  </head>
  <body>
    
    <div class="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div><br>
    <p id="f_name"></p>
    <p id="l_name"></p>
    <p id="picture"></p>
    <p id="email"></p>
    <script>
      function onSignIn(googleUser){//client information
        var profile = googleUser.getBasicProfile();
        ("ID: " + profile.getId());
        //document.getElementById("name").innerHTML = ('Name: ' + profile.getName());
        document.getElementById("f_name").innerHTML = ('First Name: ' + profile.getGivenName());
        document.getElementById("l_name").innerHTML = ('Last Name: ' + profile.getFamilyName());
        document.getElementById("picture").innerHTML = ('Picture URL: ' + profile.getImageUrl());//need to change to show actual profile picture
        document.getElementById("email").innerHTML = ("Email: " + profile.getEmail());

        // The ID token for backend:
        var id_token = googleUser.getAuthResponse().id_token;
        console.log("ID Token: " + id_token);
      };
    </script>
    
    <button onclick="signOut();">Sign out</button>
    <script>
      function signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
          document.write('User signed out.');
          //need to add a link to go back to home page
        });
      }
    </script>
    
    <div class="logo-container">
      <a href="/" class="logo-link">
        <img class="logo-image" src="static/images/search.gif" alt="Search gif">
      </a>
    </div>

    <div class="form-container">
      <form class="search-form" action="/" method="GET">
        <input class="search-field" type="text" size="100" maxlength="100" name="keywords" placeholder="Looking for something?">
        <input class="search-btn" type="submit" name="save" value="Search">
      </form>
    </div>

    <div class="top-twenty-container">
      <div class="top-twenty-content-container">
        % if top_20_keywords:
          <h3 class="top-twenty-header">TOP 20 KEYWORDS</h3>
          <table id="history">
            %for word, count in top_20_keywords.iteritems():
              <tr>
                <td>{{word}}</td>
                <td>{{count}}</td>
              </tr>
            %end
          </table>
        % else:
          <p class="empty-history">No previous searches</p>
        % end
      </div>
    </div>
  </body>
</html>