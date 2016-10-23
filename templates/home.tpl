<html>
  <head>
    <title>Search Engine</title>
    <link type="text/css" href="static/css/home.css" rel="stylesheet">
  </head>
  
  <body>

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
        % if user:
          % if history_table:
            <h3 class="top-twenty-header">RECENT SEARCH KEYWORDS</h3>
            <table id="history">
              %for word, count in history_table.iteritems():
                <tr>
                  <td>{{word}}</td>
                  <td>{{count}}</td>
                </tr>
              %end
            </table>
          % else:
            <p class="empty-history">No previous searches</p>
          % end
        % else:
          <p class="empty-history">Log in to see search history</p>
        % end
      </div>
    </div>
  </body>
</html>
