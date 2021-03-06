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
        % if suggestedsearch is None:
        <h3 class="results-search-for">Searching for "<i>{{search_string}}</i>"</h3>
        % else:
        <h3 class="results-search-for">Showing results for "<i>{{search_string}}</i>"</h3>
        <h3 class ="results-search-for">Did you mean <a href="/?keywords={{suggestedsearch}}&save=search">{{suggestedsearch}}</a></h3>
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

      <div class="results-page-numbers">
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

    </div>
  </body>
</html>
