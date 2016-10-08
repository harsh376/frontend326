<h2><a href="/">Back to Home</a></h2>
<form action="/" method="GET">
  <input type="text" size="100" maxlength="100" name="keywords" placeholder="{{search_string}}">
  <input type="submit" name="save" value="Search">
</form>
<h3>Search results for "{{search_string}}"</h3>
<div>
  <table id="results">
    <tr>
      <td>Word</td>
      <td>Count</td>
    </tr>
    %for word, count in word_count.iteritems():
      <tr>
        <td>{{word}}</td>
        <td>{{count}}</td>
      </tr>
    %end
  </table>
</div>