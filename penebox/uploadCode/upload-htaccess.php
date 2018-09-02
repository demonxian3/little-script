
   
<?php
  /* GLOBAL */
  $fileIndex = "file";
  $uploadDir = "uploadfiles";
  $denyType = array("php","asp","txt","jsp","aspx","html","asa","exe");
  $arrayLen  = count($denyType);
?>

<html>
<body style="background:#F5F5F5;">

<form action="" method="post" enctype="multipart/form-data">
  <label for="file"> Apache htaccess解析漏洞测试: </label><hr><br>
  <input value="请选择上传的文件" readonly="readonly" id="show"/>
  <input id="file" <?php echo "type='$fileIndex' name='$fileIndex'; "?> /><br />
  <input type="submit" value="上传" />
</form>

<?php

  if( $_FILES[$fileIndex]){

    $pattern = '/(\.)(.{1,8})$/';
    preg_match($pattern, $_FILES[$fileIndex]["name"],$filetype);  //index 2 is typename;

    //Restrict File Type & Size
    for( $i=0; $i<$arrayLen; $i++){
       if( $denyType[$i] == $filetype[2]){
          echo "<script>alert('上传的类型不能为 $filetype[2]')</script>";
          exit();
       }
    }

   

    if( $filetype != ""  &&  $_FILES[$fileIndex]["size"] < 200000){   //200k 

    //Show Info and Save file to tmp_file
    if ($_FILES["$fileIndex"]["error"] > 0){
       echo "Error: ".$_FILES["$fileIndex"]["error"] . "<br/>";
    }else{
       echo "名称: "   .      $_FILES["$fileIndex"]["name"]        . "<br/>";
       echo "类型: "     .      $_FILES["$fileIndex"]["type"]        . "<br/>";
       echo "大小: "     .floor($_FILES["$fileIndex"]["size"] /1024) . "KB <br/>";
       echo "临时名: ".      $_FILES["$fileIndex"]["tmp_name"]    . "<br/><br/>";
    }


    //Save tmp_file to upload/file 
    if(file_exists ("$uploadDir/" . $_FILES[$fileIndex]["name"]))
      echo $_FILES[$fileIndex] . " already exists. <br>";
    else{
      move_uploaded_file( $_FILES[$fileIndex]["tmp_name"], "$uploadDir/". $_FILES[$fileIndex]["name"]);
      echo "<p style='color:red' > <b>上传成功: </b>存储位置为" . $uploadDir."/".$_FILES[$fileIndex]['name'] . "</p>";
    }
  }else{
    echo "<script>alert('上传文件只能是图片格式')</script>";
  }
  }
?>

