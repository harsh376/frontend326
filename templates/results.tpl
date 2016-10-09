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
    </div>

    <div class="results-content">
      <div class="results-container">
        <h3 class="results-search-for">Search for "<i>{{search_string}}</i>"</h3>
        <table id="results">
          <tr class="row-headings">
            <th class="col-word">Word</th>
            <th class="col-count">Count</th>
          </tr>
          %for word, count in word_count.iteritems():
            <tr>
              <td>{{word}}</td>
              <td>{{count}}</td>
            </tr>
          %end
        </table>
    </div>
  </body>
</html>