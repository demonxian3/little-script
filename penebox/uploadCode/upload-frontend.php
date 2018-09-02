<?php
  /* GLOBAL */
  $fileIndex = "file";
  $uploadDir = "uploadfiles";

?>

<html>
<body style="background:#F5F5F5;">

<form action="" method="post" enctype="multipart/form-data">
  <label for="file"> 上传接口测试（js过滤）: </label><hr><br>
  <input value="请选择上传的文件" readonly="readonly" id="show"/>
  <input id="file" <?php echo "type='$fileIndex' name='$fileIndex'; "?> /><br />
  <input type="submit" value="上传" onclick="return CheckFile()"/>
</form>


<script>
  function CheckFile(){
    var obj = document.getElementById("file");
    var array = new Array('gif','jpeg','png','jpg');  //allow type
    if( obj.value == '' ){
      alert("文件不能为空");
      return false;
    }
    else{
       var fileContentType = obj.value.match(/^(.*)(\.)(.{1,8})$/)[3];  //get type
       for( var i in array){
         if(fileContentType.toLowerCase() == array[i].toLowerCase() )
           return true;
       }
       alert("上传的图片类型只能为: gif, jpeg, png, jpg");
       return false;
    }
  }
</script>
</body>
</html>

<?php

  if($_FILES[$fileIndex]){
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
  }
?>

