<?php
  mysql_connect('localhost:3306','root','26678742a');
  mysql_set_charset('utf8');
  mysql_select_db('intel');

  if($id = $_COOKIE['id']){
    $sql = "select * from users where id = '$id'";
    echo $sql ."<br/>";
    $res = mysql_query($sql);
    $row = mysql_fetch_assoc($res);
    if($row){ 
      echo "username is :" . $row[username] ."<br>";
      echo "remark   is :" . $row[remark]   ."<br>";
    }else{
      echo "用户不存在或无备注";
    }
  }

?>

<h3>Hello web</h3><hr><br>
This is test page;



