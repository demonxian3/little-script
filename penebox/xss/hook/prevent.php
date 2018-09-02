<!-- 
  <meta http-equiv="refresh" content="5;url=http://www.baidu.com"/>
-->

<script>
 var _alert = alert;
 window.alert = function(str){
   _alert("小屁孩，想在这里玩xss?")  //篡改alert;
   var img = new Image();
   img.style.width = img.style.height = 0;
   img.src = "http://118.89.51.198/lzx/XSS/hook/record.php?data="+str;
 }
</script>
<html>
<body>
<form action="<?php echo $_SERVER[PHP_SELF];?>" method="POST">
  Your name: <input type="text" name="username"><br>
  Your emial: <input type="text" name="usermail"<br>
  <input type="submit" value="submit">
</form>

<?php
  if($_POST[username])echo "Your name is  $_POST[username]<br>";
  if($_POST[usermail])echo "Your mail is $_POST[usermail]<br>";
  if($_GET[id])echo "I get the id is $_GET[id]<br>";
  if($_COOKIE[USERID])echo "Your cookie is $_COOKIE[USERID]";
  
  $_GET[divId] ? $id = $_GET[divId] : $id = 0;
  echo "<h3>This is div have xss </h3><hr><br>";
  echo "<div id=$id style=\"border:1px solid red;width:100px;height:100px\" ></div>";
?>

</body>
</html>
