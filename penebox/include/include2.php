<?php  
    $file = $_GET['file'];  
    $path = "/var/www/html/$file.php";
    echo $path."<br>";
    if (file_exists($path)){  
        //echo 'include /var/www/html/'.$file.'.php';  
        //include "/var/www/html/{$file}.php";  
        include "/etc/passwd";
    }else{
        echo '/var/www/html/'.$file.'.php is not exist\n';
    }  
?>
