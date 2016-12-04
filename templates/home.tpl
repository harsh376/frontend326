<html>
  <head>
    <title>Search Engine</title>
    <link type="text/css" href="static/css/home.css" rel="stylesheet">

    <script>
      function showResult(search_query) {
        if (search_query.length === 0) {
          document.getElementById("livesearch").innerHTML="";
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
          }
        }

        var url = '/autocomplete?search_query='.concat(search_query)
        xmlhttp.open('GET', url, true);
        xmlhttp.send();
      }
    </script>

  </head>
  
  <body>

    <div class="home-login-status-container">
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

    <div class="logo-container">
      <a href="/" class="logo-link">
        <img class="logo-image" src="static/images/search.gif" alt="Search gif">
      </a>
    </div>

    <div class="form-container">
      <form class="search-form" action="/" method="GET">
        <input class="search-field" type="text" size="100" maxlength="100" name="keywords" placeholder="Looking for something?" onkeyup="showResult(this.value)" autocomplete="off">
        <input class="search-btn" type="submit" name="save" value="Search">
        <div id="livesearch"></div>
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
