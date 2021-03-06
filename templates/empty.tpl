<html>
  <head>
    <title>Search Results</title>
    <link type="text/css" href="static/css/results.css" rel="stylesheet">

    <script>
      function showResult(search_query) {
        if (search_query.length === 0) {
          document.getElementById("livesearch").innerHTML="";
          var headerHeight = document.getElementById('results-header').offsetHeight;
          console.log(headerHeight);
          document.getElementById('results-content').style.top = headerHeight;
          return;
        }

        var xmlhttp;

        if (window.XMLHttpRequest) {
          // code for IE7+, Firefox, Chrome, Opera, Safari
          xmlhttp=new XMLHttpRequest();
        } else {  // code for IE6, IE5
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }


        xmlhttp.onreadystatechange = function() {
          if (this.readyState==4 && this.status==200) {
            var response = JSON.parse(this.responseText);
            var elements = response.elements;


            document.getElementById('livesearch').innerHTML=elements;
            document.getElementById("livesearch").style.border="1px solid #A5ACB2";

            var headerHeight = document.getElementById('results-header').offsetHeight;
            console.log(headerHeight);
            document.getElementById('results-content').style.top = headerHeight;
          }
        }

        var url = '/autocomplete?search_query='.concat(search_query)
        xmlhttp.open('GET', url, true);
        xmlhttp.send();
      }
    </script>


  </head>

  <body>
    <div id="results-header" class="results-header">

      <div class="results-logo-container">
        <a href="/" class="results-logo-link">
          <img class="results-logo-image" src="static/images/logo.png" alt="Logo">
        </a>
      </div>

      <div class="results-form-container">
        <form action="/" method="GET">
          <input class="results-search-field" type="text" size="100" maxlength="100" name="keywords" value="{{search_string}}" onkeyup="showResult(this.value)" autocomplete="off">
          <input class="results-search-btn" type="submit" name="save" value="Search">
          <div id="livesearch"></div>
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

    <div id="results-content" class="results-content">
      <div class="results-container">
        <h3 class="results-search-for">No Results found for "<i>{{search_string}}</i>"</h3>
        % if suggestedsearch is not None:
        <h3 class ="results-search-for">Did you mean <a href="/?keywords={{suggestedsearch}}&save=search">{{suggestedsearch}}</a></h3>
        % end
    </div>
  </body>
</html>