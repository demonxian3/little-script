
<link rel="stylesheet" href="../bootstrap/css/bootstrap.min.css"/>
<script src="../bootstrap/js/bootstrap.min.js"></script>

<div class="container"> <br><br><br>
<div class="jumbotron">  
  <h2 class="text-center text-primary" >免费Ping测试</h2><hr>
  <form role="form" action="" method="post">
  <label for="name " style="font-size:19px;display:inline" class="text-warning" >请输入： </label>
  <input name="ipaddr" style="width:330px;display:inline" type="text" class="form-control" value="<?php echo $_POST['ipaddr'];?>" id="name" placeholder="主机地址">
  <button type="submit" style="display:inline" class="btn btn-default">Go</button>
  </form>
  <div style="width:1000px;height:300px;background:white;text-indent:0px;background:#F5F5F5;overflow:scroll">
  <pre style="border:none" >
  <?php
  if($_POST["ipaddr"]){
    $ipaddr = $_POST["ipaddr"];
     $pattern_url = "^([a-zA-Z0-9]+\.)*([a-zA-Z0-9]+\.)([a-zA-Z]+)$";        //匹配域名
     $pattern_ip  = "^([1-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([1,9]{1,3})$"; 				//匹配IP地址
    if( ereg($pattern_url,$ipaddr) || ereg($pattern_ip,$ipaddr)){
      $command = "ping -c 4 $ipaddr ";
      echo "<script>alert('".$command."')</script>";
      echo shell_exec($command); 
    }else{
      echo "输入的IP地址不合法";
    }
  }
  ?>
  </pre>
  </div>
</div>
</div>
