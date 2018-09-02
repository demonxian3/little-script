<?php
if($_GET[file])$file = $_GET[file];
if($_GET[dir])$dir = $_GET[dir];
else $dir = ".";

$path = "$dir/$file";

if(!is_file($path)){
  echo "The file isn't exited";
  exit();
}else{

  $file=fopen("$path","r") or die("Cannot open the file");
  header("Content-Type: application/octet-stream");
  header("Accept-Ranges: bytes");
  header("Accept-Length: ".filesize("$path"));
  header("Content-Disposition: attachment; filename=".$file);
  echo fread($file,filesize("$path"));

  fclose($file);
}
?>
