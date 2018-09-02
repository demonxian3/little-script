<?php
  if($filename = $_GET[filename]){
    if(is_file($filename)){
      header("Content-Disposition: attachment; filename=$filename");
    }else{
      echo "请求的文件不存在";
      exit();
    }
  }
  echo "任意文件下载测试页面<br>";
?>
<a href="test.php?filename=b.png">下载b.png</a><br>
<a href="ck.rar">下载ck.rar</a><br>
<a href="test.php?filename=./important/passwd">下载important/passwd</a><br>
<a href="test.php?filename=./important/hosts">下载important/hosts</a><br>
<a href="test.php?filename=./important/resolv.conf">下载important/reslov.conf</a><br>
  

