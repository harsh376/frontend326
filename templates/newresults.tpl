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
        <h3 class="results-search-for">Search for "<i>{{search_string}}</i>"</h3>
        <p class="results-search-for"><i>Page {{currentPage}} of {{val}} results</i></p>
          %for word in result:
          <div>
              <div class="results-container">{{word[0]}}</div>
              <div class="results-container">
                <a href="{{word[1]}}" target="_blank">{{word[1]}}</a>
              </div>
              <div class="results-container">{{word[2]}}</div>
              <br>
          </div>
          %end
    </div>

    <div>
      <form action={{url}} method="POST">
        % if currRow == 0:      
          <button name="nav" value="prevPage" disabled>&lt;</button>
        % else:
          <button name="nav" value="prevPage">&lt;</button>
        % end

        % for num in range:
          <button name="nav" value="{{num}}">{{num}}</button>
        %end

        % if (currRow+10) >= val:
          <button name="nav" value="nextPage" disabled>&gt;</button>
        % else:
          <button name="nav" value="nextPage">&gt;</button>
        % end

      </form>
    </div>
  </body>
</html>