<?php
mysql_connect('localhost:3306','root','26678742a');
mysql_set_charset('utf8');
mysql_select_db('penetration'); 
$username = $_GET['username'];
$sql1 = "select id,username,password from users where username = \"$username\"";
$res1 = mysql_query($sql1);
$row1 = mysql_fetch_assoc($res1);
if($row1){
  $sql2 = "select title,author,article from message where author = \"$username\"";
  $res2 = mysql_query($sql2);
}

echo $sql1 ."<br>";
echo $sql2 ."<br>";
?>

<link rel="stylesheet" href="../bootstrap/css/bootstrap.min.css">
<script src="../bootstrap/js/bootstrap.min.js"></script>
<div class="container">
<h2 class="page-header">发表文章系统查询</h2>
<div class="jumbotron">
   
<?php 
#  var_dump($row1);
  if(!$row1)echo "<p><b class='text-danger'>查无此用户</b></p>";
  else
    echo "<p>当前用户名是：<b class='text-success'>$username</b> </p><hr/>";
  
?>
    <form role="form" action="" method="get">
      <div class="form-group">
         <label for="name">输入查询的用户名:  &nbsp;&nbsp;</label>
         <input style="width:330px;display:inline;" type="text" class="form-control" id="name" placeholder="" name="username" >
	 <button type="submit" class="btn btn-default">ok</button>
      </div>
    </form>
    <div class="form-group">
         <label for="name">文本框</label>
         <textarea class="form-control" rows="30">
<?php 
    if($row1){
        $i=1;
        echo "\n";
		while($row2 = mysql_fetch_assoc($res2)){
            echo "第 $i 篇文章:\n";
		    echo "---------------------------------------------\n";
		    echo "title:  " . $row2[title]  ."\n";
		    echo "author: " . $row2[author] ."\n";
		    echo "date:   " . $row2[ctime]  ."\n";
		    echo "comment:" . $row2[comment]."\n";
		    echo "article:" . $row2[article]."\n\n";
            $i++;
		}
    }

?>
         </textarea>
    </div>

</div>
</div>

