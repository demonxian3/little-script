<?php
  session_start();
  mysql_connect('localhost:3306','root','26678742a');
  mysql_set_charset('utf8');
  mysql_select_db('penetration');
  
  //check login
  if($_POST[username] && $_POST[password]){
    $username = $_POST['username'];
    $password = md5($_POST['password']);
    $login_sql = "select * from users where username = '$username' and password = '$password'";
    $login_res = mysql_query($login_sql);
    $login_row = mysql_fetch_assoc($login_res);
    if($login_row){
      $_SESSION[remark] = $login_row[remark];
      $_SESSION[id] = $login_row[id];
      $_SESSION[username] = $username;
      echo "<script>window.location='StorageType-main.php'</script>";
    }else{
      echo "<script>alert('Login Failed!')</script>";
    }
  }
?>

<form action="<?php echo $_SERVER[PHP_SELF]?>" method="post">
 username: <input name="username"/><br>
 password: <input name="password" type="password" />
 <input type="submit" value="login" />
</form>
