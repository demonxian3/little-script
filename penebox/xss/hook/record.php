<?php
  if($_GET[data]){
    $myfile = fopen("attack.txt","a+") or die("cannot open the file");
    
    $content = "";

    $date =  date("Y/m/d H:i:s",$_SERVER[REQUEST_TIME]) ;
    $addr =  $_SERVER[REMOTE_ADDR];
    $file =  $_SERVER[PHP_SELF];
    $cont =  $_GET[data];

    $content = "$date  $addr  $file  $cont \n";
    
    fwrite($myfile,$content);
    fclose();
  }
?>
