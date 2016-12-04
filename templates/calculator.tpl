<html>
    
    <head>
        <meta charset="UTF-8">
        <title>Calculator</title>
        <link rel="stylesheet" href="static/css/calculator.css" media="screen" type="text/css" />
        <link type="text/css" href="static/css/results.css" rel="stylesheet">"static/css/style.css" media="screen" type="text/css" />
        <script src="static/js/index.js"></script>
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
        <table id="calculator">
          <tr>
            <td colspan="7">
              <input type="text" id="display" value="{{value}}" />
            </td>
          </tr>
          <tr>
            <td>
              <input id="btnAns" type="button" name="operator" value="CE" onclick="ce()"/>
            </td>
            <td>
              <input id="btnPi" type="button" name="operator" value="π" onclick="set('3.14')" />
            </td>
            <td>
              <input id="btnE" type="button" name="operator" value="e" onclick="set('2.718281828')" />
            </td>
            <td>
              <input id="btnOParen" type="button" name="operator" value="(" onclick="set('(')" />
            </td>
            <td>
              <input id="btnCParen" type="button" name="operator" value=")" onclick="set(')')" />
            </td>
            <td>
              <input id="btnPcnt" type="button" name="operator" value="%" onclick="percent()" />
            </td>
            <td>
              <input id="btnCE" type="button" name="operator" value="DEL" onclick="del()" />
            </td>
          </tr>
          <tr>
            <td>
              <input id="btnRad" type="button" name="operator" value="rad" onclick="radians()"/>
            </td>
            <td>
              <input id="btnDeg" type="button" name="operator" value="deg" onclick="degrees()"/>
            </td>
            <td>
              <input id="btnFact" type="button" name="operator" value="x!" onclick="fact()" />
            </td>
            <td>
              <input id="btn7" type="button" value="7" onclick="set('7')" />
            </td>
            <td>
              <input id="btn8" type="button" value="8" onclick="set('8')" />
            </td>
            <td>
              <input id="btn9" type="button" value="9" onclick="set('9')" />
            </td>
            <td>
              <input id="btnDiv" type="button" name="operator" value="÷" onclick="set('/')" />
            </td>
          </tr>
          <tr>
            <td>
              <input id="btnSineInv" type="button" name="operator" value="asin" onclick="asine()" />
            </td>
            <td>
              <input id="btnSine" type="button" name="operator" value="sin" onclick="sine()" />
            </td>
            <td>
              <input id="btnLN" type="button" name="operator" value="ln" />
            </td>
            <td>
              <input id="btn4" type="button" value="4" onclick="set('4')" />
            </td>
            <td>
              <input id="btn5" type="button" value="5" onclick="set('5')" />
            </td>
            <td>
              <input id="btn6" type="button" value="6" onclick="set('6')" />
            </td>
            <td>
              <input id="btnMul" type="button" name="operator" value="×" onclick="set('*')" />
            </td>
          </tr>
          <tr>
            <td>
              <input id="btnCosInv" type="button" name="operator" value="acos" onclick="acosine()" />
            </td>
            <td>
              <input id="btnCos" type="button" name="operator" value="cos" onclick="cosine()" />
            </td>
            <td>
              <input id="btnLog" type="button" name="operator" value="log" onclick="fLog()" />
            </td>
            <td>
              <input id="btn1" type="button" value="1" onclick="set('1')" />
            </td>
            <td>
              <input id="btn2" type="button" value="2" onclick="set('2')" />
            </td>
            <td>
              <input id="btn3" type="button" value="3" onclick="set('3')" />
            </td>
            <td>
              <input id="btnSub" type="button" name="operator" value="-" onclick="set('-')" />
            </td>
          </tr>
          <tr>
            <td>
              <input id="btnTanInv" type="button" name="operator" value="atan" onclick="atangent()" />
            </td>
            <td>
              <input id="btnTan" type="button" name="operator" value="tan" onclick="tangent()" />
            </td>
            <td>
              <input id="btnSqrt" type="button" name="operator" value="√" onclick="sqrRoot()" />
            </td>
            <td>
              <input id="btn0" type="button" value="0" onclick="set('0')" />
            </td>
            <td>
              <input id="btnPeriod" type="button" value="." onclick="set('.')"/>
            </td>
            <td>
              <input id="btnEqual" type="button" name="equal" value="=" onclick="answer()" />
            </td>
            <td>
              <input id="btnAdd" type="button" name="operator" value="+" onclick="set('+')" />
            </td>
          </tr>
        </table>
      </div>
    </body>

</html>