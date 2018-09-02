<form action="" method="get">
  Enter the password:
  <input name="password" />
  <input type="submit" value="Ok" />
</form>
<?php
require "flag.php";
if (isset ($_GET['password'])) {
    if (ereg("^[a-zA-Z0-9]+$",$_GET['password']) === FALSE)    
       {
        echo "first wall: You password must be alphanumeric, your input => $_GET[password]<br>";
    }
    else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)
    {
        if (strpos ($_GET['password'], '*-*') !== FALSE)
        {
            die('Flag: ' . $flag . "<br> your input =>> $_GET[password]");
        }
        else
        {
            echo("<p>*last wall: *-* have not been found and your input : $_GET[password]</p>");
        }
    }
    else
    {
        echo '<p>Second wall: The length of password  must be lesser than 8 and The value of password must be greater than 9999999 </p>';
        echo "your input -> $_GET[password]<br>";
    }
}
?>
