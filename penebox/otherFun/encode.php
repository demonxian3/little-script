<?php
function htmlencode($str){
   if(empty($str)) return;
   if($str == "") return;
   $str = str_ireplace("<","",$str);
   $str = str_ireplace(">","",$str);
   $str = str_ireplace("script","",$str);
   $str = str_ireplace("img","",$str);
   $str = str_ireplace(":","",$str);
   $str = str_ireplace("javascript","",$str);
   return $str;
}
 
if(!array_key_exists ("name",$_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){
   $isempty = true;
} else {
   $html .= '<pre>';
   $html .= '<a onclick=" '. htmlencode($_GET['name']).'">click this url</a>';
   $html .= '</pre>';
}
?>
 
<html>
<script>
</script>
</html>
