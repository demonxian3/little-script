<html>
<body>

<form action="<?php echo $_SERVER[PHP_SELF]?>" method="post">
Name: <input type="text" name="name"><br>
E-mail: <input type="text" name="email"><br>
<input type="submit">
</form>

This is GET:  <?php echo $_GET["name"]; ?> <br>
This is POST: <?php echo $_POST["name"]; ?> <br>
This is COOKIE: <?php echo$_COOKIE["name"];?> <br>

</body>
</html>
