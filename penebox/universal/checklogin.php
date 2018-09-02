<?php

  session_start();
  mysql_connect('localhost:3306','root','26678742a');
  mysql_set_charset('utf8');
  mysql_select_db('penetration');

  $username = $_POST['usernm'];
  $password =md5($_POST['passwd']);


  //$sql = 'select username,password from users where username = \"'.$username.'\" and password = \"'.$password.'\"';
  $sql = "SELECT username,password FROM users WHERE username = '$username' AND password = '$password'";
  //$sql = "SELECT username,password FROM users WHERE username = '$_POST[username]' AND password = '$_POST[password]'";

echo $sql;

$res = mysql_query($sql);

if($row = mysql_fetch_row($res)){
   echo "<script>alert('login successfully')</script>";
}else{
   echo "login failed";
}
?>
