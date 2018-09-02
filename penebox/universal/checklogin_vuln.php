<?php

  session_start();
  mysql_connect('localhost:3306','root','26678742a');
  mysql_set_charset('utf8');
  mysql_select_db('penetration');

  $username = $_POST['usernm'];
  $password =md5($_POST['passwd']);

  $sql = "SELECT id FROM users WHERE username = '$username'";
  $res = mysql_query($sql);
  //echo $sql;          //debug
  
  if($row = mysql_fetch_row($res)){
     $sql = "SELECT id FROM users WHERE password = '$password'";
     $res = mysql_query($sql);
     if($row = mysql_fetch_row($res))
         echo "<script>alert('login successfully')</script>";
     else
        echo "login failed";
  }else
     echo "login failed";
?>
