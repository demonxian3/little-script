<?php
  session_start();
  if(!$_SESSION[username]){
    echo "Need to login";
    exit;
  }else{
    mysql_connect('localhost:3306','root','26678742a');
    mysql_set_charset('utf8');
    mysql_select_db('penetration');


    //如果接到POST请求:
    if($_POST['remark']){
      $sql = "update users set remark = '$_POST[remark]' where id = $_SESSION[id]";
      $res = mysql_query($sql);
      if($res)echo "<script>alert('Success')</script>";
      else echo "<script> alert('Update failed')</script>";
    }

    echo "Welcome, ".$_SESSION[username];
    echo "<br>Your remark is: ".$_SESSION[remark];
?>


  <form name="tags" id="tags" method='post' action='<?php echo $_SERVER[PHP_SELF]?>'>
  Update the remark: 
  <input name="remark"><br>
  <input type="submit" value="Ok"/>
  </form>

<?php
    //如果是管理员登陆
    if($_SESSION[id] == 1){
      echo "Users Manage System<hr>";
      $query = "select id,username,remark from users";
      $res = mysql_query($query);
      echo "<table><tr><td width='30px'>ID</td><td width='100px'>username</td><td>remark</td></tr>";
      while($row = mysql_fetch_assoc($res))  
        echo "<tr><td>$row[id]</td><td>$row[username]</td><td>$row[remark]</td></tr>";
      echo "</table>";
    }
      
  }
?>
