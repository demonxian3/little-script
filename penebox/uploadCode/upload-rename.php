<?php
  /* GLOBAL */
  $fileType = "";
  $fileIndex = "file";
  $uploadDir = "uploadfiles";
  $allowType = array("image/gif","image/jpeg","image/pjpeg");
  $arrayLen  = count($allowType);
  $timestamp = time();
?>

<html>
<body style="background:#F5F5F5;">

<form action="" method="post" enctype="multipart/form-data">
  <label for="file"> 上传接口测试（重命名规则）: </label><hr><br>
  <input value="请选择上传的文件" readonly="readonly" id="show"/>
  <input id="file" <?php echo "type='$fileIndex' name='$fileIndex'; "?> /><br />
  <input type="submit" value="上传" />
</form>

<?php

  if( $_FILES[$fileIndex]){
    //Restrict File Type & Size
    for( $i=0; $i<$arrayLen; $i++){
       if( $allowType[$i] == $_FILES[$fileIndex]["type"]){
          $fileType = $allowType[$i];
          break;
       }
    }

    if( $fileType != ""  &&  $_FILES[$fileIndex]["size"] < 200000){   //200k 

      //Show Info and Save file to tmp_file
      if ($_FILES["$fileIndex"]["error"] > 0){
        echo "Error: ".$_FILES["$fileIndex"]["error"] . "<br/>";
      }else{
        echo "名称: "   .      $_FILES["$fileIndex"]["name"]        . "<br/>";
        echo "类型: "     .      $_FILES["$fileIndex"]["type"]        . "<br/>";
        echo "大小: "     .floor($_FILES["$fileIndex"]["size"] /1024) . "KB <br/>";
        echo "临时名: ".      $_FILES["$fileIndex"]["tmp_name"]    . "<br/><br/>";
      }

      //Rename the file
      $filename = $_FILES[$fileIndex]["name"];
      $pattern = '/(\..{1,6})$/';
      preg_match($pattern,$filename,$imagetypes);
      $filename =  $timestamp."".$imagetypes[0];

      //Save tmp_file to upload/file 
      if(file_exists ("$uploadDir/" . $filename))
        echo $_FILES[$fileIndex]["name"] . " already exists. <br>";
      else{
        move_uploaded_file( $_FILES[$fileIndex]["tmp_name"], "$uploadDir/$filename");
        echo "<p style='color:red'>Upload successfully:</p> Save path = $uploadDir/$filename ";
      }
    }else{
      echo "<script>alert('上传的文件类型只支持图片格式')</script>";
    }
  }
?>
