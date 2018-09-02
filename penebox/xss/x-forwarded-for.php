<?php
  echo "This is the  x-forwarded-for.php test page <br>";
  $cip = getenv ( 'HTTP_CLIENT_IP' );
  $xip = getenv ( 'HTTP_X_FORWARDED_FOR' );
  $rip = getenv ( 'REMOTE_ADDR' );
  echo " HTTP_CLIENT_IP = $cip  <br>";
  echo " HTTP_X_FORWARDED_FOR = $xip <br>";
  echo " REMOTE_ADDR = $rip <br>";
?>
