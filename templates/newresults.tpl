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
          % if oldsearch is None:
          <input class="results-search-field" type="text" size="100" maxlength="100" name="keywords" value="{{search_string}}">
          % else:
          <input class="results-search-field" type="text" size="100" maxlength="100" name="keywords" value="{{oldsearch}}">
          %end
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
        % if oldsearch is None:
        <h3 class="results-search-for">Searching for "<i>{{search_string}}</i>"</h3>
        % else:
        <h3 class="results-search-for">Showing results for "<i>{{search_string}}</i> instead of <i>{{oldsearch}}</i>"</h3>
        <!--<h3 class="results-search-for">Search instead for "<i>{{oldsearch}}</i>"</h3>-->
        %end
        <p class="results-search-for"><i>Page {{currentPage}} of {{val}} results</i></p>
          %for word in result:
          <div>
              <div class="results-container"><b>{{word[0]}}</b></div>
              <div class="results-container">
                <a href="{{word[1]}}" target="_blank">{{word[1]}}</a>
              </div>
              <div class="results-container">{{word[2]}}</div>
              %if missingwords is not None:
              <div class="results-container">
                <i>Missing </i>
                %for miss in missingwords:
                <strike>{{miss}} </strike>
                %end
              </div>
              %end
          </div>
          <br/>
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

    <div>
        % if suggestedsearch is not None:
           <h4>Did you mean"</h4>
           %for word in suggestedsearch:
                <a href="/?keywords={{word}}&save=search">{{word}} </a>
           %end
        %end
    </div>
  </body>
</html>
