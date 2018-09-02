<?php
mysql_connect('localhost:3306','root','26678742a');
mysql_set_charset('utf8');
mysql_select_db('intel'); 
?>

<form name="tags" id="tags" method='post' action=''>
Input your name:
<input name="username"><br> 
<input type="submit" value="Ok"/>
</form>
你的备注是:
<?php
  if($_POST['username']){
    $sql = "select remark from users where username = '$_POST[username]'";
    $res = mysql_query($sql);
    $row = mysql_fetch_assoc($res);
    if($row){
      echo $row[remark];
    }else{
      echo "用户不存在或无备注";
    }
  }
?>
