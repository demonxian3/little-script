<h3>About: Json</h3><hr>

<?php

  $student = $_POST[student];
  $student = json_decode($student,true);
  echo "Application/x-www-form-urlencoded: <br>";
  print_r($student);
  echo "<br><br><hr>";
  echo "Application/json: <br>";
  echo "\$GLOBALS['HTTP_RAW_POST_DATA']:";
  var_dump($GLOBALS["HTTP_RAW_POST_DATA"]);
  echo "<br><br>file_get_contents: <br>";
  var_dump(file_get_contents('php://input'));

?>
