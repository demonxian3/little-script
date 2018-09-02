<!DOCTYPE html>
<html>
<head>
   <meta charset="gbk2312">
   <title>宽字节注入</title>
</head>
<body>
<?php
  
  if(isset($_GET['id'])){
    $id = $_GET['id'];
    
    $conn = mysql_connect('localhost:3306','root','26678742a');
    mysql_select_db('intel',$conn);
    mysql_query("set charset gbk");
    //defense code
    $id = str_replace("'", "\'", $id);
    $sql = "SELECT * FROM users WHERE id = '{$id}'";
    echo "你当前执行的sql语句是：";
    echo $sql . "<hr>";

    $res = mysql_query($sql);
    $row = mysql_fetch_array($res);

    if(isset($row)){
    	echo "用户ID： " .$row[0]. "<br/>";
    	echo "用户名： " .$row[1]. "<br/>";
    	echo "用户密码： ".$row[2]. "<br/>";
    }

    print_r(mysql_error());
    #mysql_query("set charset utf8");

  }else{
    echo "请给个ID参数";
  }
  
?>
</body>

</html>

