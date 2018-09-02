<script>
  var _A = alert;
  window.alert = function(a){
    _A("玩你妈逼的XSS，快滚去睡觉!!\n")
  }
</script>
<html>

<?php
   
   if(!$_GET[id])$_GET[id]=0;
   echo "<h3>Article-$_GET[id]</h3><hr>";
   switch($_GET[id]){
     case 0:
       echo "No id parameter for request";
       break;

     case 1:
       echo "hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world ";
        break;

      case 2:
        echo "good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning good morning ";
        break;
   
      case 3:
         echo "thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you thank you ";
         break; 
   }
?>
