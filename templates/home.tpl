<h2><a href="/">Search Engine</a></h2>
<form action="/" method="GET">
  <input type="text" size="100" maxlength="100" name="keywords" placeholder="Search for something">
  <input type="submit" name="save" value="Search">
</form>
<h3>Top 20 Keywords</h3>

% if top_20_keywords:
  <div>
    <table id="history">
      <tr>
        <td>Word</td>
        <td>Count</td>
      </tr>
      %for word, count in top_20_keywords.iteritems():
        <tr>
          <td>{{word}}</td>
          <td>{{count}}</td>
        </tr>
      %end
    </table>
  </div>
% else:
  <div>No search history available</div>
% end