<!DOCTYPE html>
<html>
<head>
    <title>后台登录</title>
</head>
<body>
    <form action="" method="post">
        <h1>后台登录</h1>
        <br>账号：<input type="text" name="user">
        <br>密码：<input type="password" name="pass">
        <input type="submit" value="登录">
    </form>
</body>
</html>
<?php
$user=@$_POST["user"];
$pass=@$_POST["pass"];
if($user!==null){
    if($user=="admin"){
        if($pass=="admin123"){
            header("Location: ./success.php");
        }else{
            echo "<script>alert('登录错误')</script>";
        }
    }else{
        echo "<script>alert('登录错误')</script>";
    }
}
?>