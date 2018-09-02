<h3>Welcome to the php-include file test page</h3><hr>
<p>
  Parameter: filename;<br>
  method: GET;<br>
  directory: include;<br>
  function: include<br>
</p>

<?php
  $file = $_GET["filename"];
  include($file);
?>
