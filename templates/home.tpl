<html>
  <head>
    <title>Search Engine</title>
    <link type="text/css" href="static/css/home.css" rel="stylesheet">
  </head>
  <body>
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
            <tr class="row-headings">
              <th class="col-word">Word</th>
              <th class="col-count">Count</th>
            </tr>
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
