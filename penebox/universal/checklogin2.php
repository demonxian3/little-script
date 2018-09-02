<?php

  session_start();
  mysql_connect('localhost:3306','root','26678742a');
  mysql_set_charset('utf8');
  mysql_select_db('race');

  $usernm = $_POST['usernm'];
  $passwd =md5($_POST['passwd']);

  #race
  $sql = "select * from users where usernm = '$usernm'";

echo $sql;

$res = mysql_query($sql);
$row = mysql_fetch_assoc($res);

//var_dump($row[passwd]);
//if($row[passwd] == md5($passwd))echo "YES";
//else echo "No";
echo "<br> \$row[passwd] = ".$row[passwd]." ; <br/>";

echo "input = ". $passwd;
#race
if($row[passwd] == $passwd){
  echo "<script>alert('login successfully')</script>";
  ///var_dump($row);
}else{
  echo "Login Failed";
}

?>
