<html>
  <head>
    <title>Search Results</title>
    <link type="text/css" href="static/css/results.css" rel="stylesheet">
  </head>

  <body>
    <div class="results-header">

      <div class="results-logo-container">
        <a href="/" class="results-logo-link">
          <img class="results-logo-image" src="static/images/logo.png" alt="Logo">
        </a>
      </div>

      <div class="results-form-container">
        <form action="/" method="GET">
          <input class="results-search-field" type="text" size="100" maxlength="100" name="keywords" value="{{search_string}}">
          <input class="results-search-btn" type="submit" name="save" value="Search">
        </form>
      </div>

      <div class="results-login-status">
        % if user != None:
          <div>{{user.get('email')}}</div>
          <div>
            <a href="/logout">Log out</a>
          </div>
        % else:
          <div>
            <a href="/login/google">
              <img src="static/images/google_signin.png" alt="Sign in">
            </a>
          </div>
        % end
      </div>

    </div>

    <div class="results-content">
      <div class="results-container">
        <h3 class="results-search-for">No Results found for "<i>{{search_string}}</i>"</h3>
        % if suggestedsearch is not None:
        <h3 class ="results-search-for">Did you mean <a href="/?keywords={{suggestedsearch}}&save=search">{{suggestedsearch}}</a></h3>
        % end
    </div>
  </body>
</html>