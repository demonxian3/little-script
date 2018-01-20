<?php
# @Auth: Demon
# @Date: 2018-1-20
# @Vers: 1.0
# @Desc: Storage ScoreData of student to Mysql from SZISA;

extract($_GET);

mysql_connect("localhost","root","yourpasswd") or die('Can\'n connect Mysql');  //FIX1
mysql_select_db("School");
mysql_set_charset("utf8");

/*
CREATE TABLE `AverageData` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userID` int(200) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `h161701` varchar(30) DEFAULT NULL,
  `h161702` varchar(30) DEFAULT NULL,
  `h171801` varchar(30) DEFAULT NULL,
  `h171802` varchar(30) DEFAULT NULL,
  `i1617` varchar(30) DEFAULT NULL,
  `i1718` varchar(30) DEFAULT NULL,
  `u1617` varchar(30) DEFAULT NULL,
  `u1718` varchar(30) DEFAULT NULL,
  `f1617` varchar(30) DEFAULT NULL,
  `f1718` varchar(30) DEFAULT NULL,
  `all` varchar(30) DEFAULT NULL,
  `all-school` varchar(30) DEFAULT NULL,
  `pass` varchar(30) DEFAULT NULL,
  `unpass` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8

CREATE TABLE `ScoreData` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userID` int(200) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `semester` varchar(255) DEFAULT NULL,
  `score` varchar(50) DEFAULT NULL,
  `courseID` int(100) DEFAULT NULL,
  `courseName` varchar(255) DEFAULT NULL,
  `courseWay` varchar(100) DEFAULT NULL,
  `courseType` varchar(100) DEFAULT NULL,
  `courseScore` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1500 DEFAULT CHARSET=utf8

*/


/* CHECK FUNCTION  */      		#if php version<5.4 , define function:gzdecode
if(!function_exists('gzdecode')){
  function gzdecode($data){
    return gzinflate(substr($data,10,-8));
  }
}


if(!isset($studentNum))$studentNum = 1601050101;
// Get 请求
/* FORGE HEADER */
$Headers = array();
$Headers[] = "Host: api.wx.sxisa.com";
$Headers[] = "User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:56.0) Gecko/20100101 Firefox/56.0";
$Headers[] = "Accept: application/json, text/plain, */*";
$Headers[] = "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3";
$Headers[] = "Accept-Encoding: gzip, deflate, br";
$Headers[] = "Referer: https://score.m.sxisa.com/?n=$studentNum";
$Headers[] = "Origin: https://score.m.sxisa.com";
$Headers[] = "X-Forwarded-For: 172.16.1.128";
$Headers[] = "Connection: keep-alive";
$Headers[] = "Pragma: no-cache";
$Headers[] = "Cache-Control: no-cache";
$TargetUrl = "https://api.wx.sxisa.com/score/$studentNum";

/*  Main Function */
$Response = sendGetRequest($TargetUrl,$Headers);
$ExtractData = gzdecode($Response);
$res = json_decode($ExtractData);

class ScoreObj{}
class Average{}

$sc = new ScoreObj();
$av = new Average();

$i = 0;
$j = 0;

//重构数据结构
foreach($res->result as $title => $value){
  if(preg_match("/学期/",$title)){

    echo $title."<br><table border='1'>";

    if(!isset($queryName)){			//姓名
	$queryName = $value[0]->username;
	$av->username = $value[0]->username;
	$sc->username = $value[0]->username;
    }
    if(!isset($queryID)){  			//学号
	$queryID = $value[0]->userid;
	$av->userID = $value[0]->userid;
	$sc->userID = $value[0]->userid;
    }

    foreach($value as $item){
      echo "<tr>
            <td style='width:200px'>$item->course_name	</td>
            <td style='width:60px'> $item->total	</td>
            <td style='width:80px'> $item->course_type	</td>
            <td style='width:60px'> $item->method	</td>
            <td style='width:40px'> $item->credit	</td>
            <td style='width:90px'> $item->course_code	</td>
            <tr>";

           $sc->data[$i]->courseName  =  $item->course_name ;
           $sc->data[$i]->score       =  $item->total       ;
           $sc->data[$i]->courseType  =  $item->course_type ;
           $sc->data[$i]->courseWay   =  $item->method      ;
           $sc->data[$i]->courseScore =  $item->credit      ;
           $sc->data[$i]->courseID    =  $item->course_code ;
           $sc->data[$i]->semester = $title;

           $i++;
    }
    echo "</table>";
  }
  
  else if(preg_match("/^平均分$/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
	$av->data[$j++]=$score;
     }
  }

  else if(preg_match("/学年/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
	$av->data[$j++]=$score;
     }
  }

  else if(preg_match("/总评/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
	$av->data[$j++]=$score;
     }
  }
  
}//foreach Restructure

/* Insert Data to Mysql */
$len = sizeof($sc->data);
for($i=0;$i<$len;$i++){
  $userID      = $sc->userID;
  $username    = $sc->username;
  $semester    = $sc->data[$i]->semester;
  $score       = $sc->data[$i]->score;
  $courseID    = $sc->data[$i]->courseID;
  $courseName  = $sc->data[$i]->courseName;
  $courseWay   = $sc->data[$i]->courseWay;
  $courseType  = $sc->data[$i]->courseType;
  $courseScore = $sc->data[$i]->courseScore;
  
  $sel = "select id from ScoreData where userID = '$userID' and courseID = '$courseID' ";
  $res = mysql_query($sel);
  $row = mysql_fetch_assoc($res);
  if($row){					//判断数据是否存在
     var_dump($row);
     echo "[Score]data is already existed <br>";	//如果存在弹出消息
  }
  else{
    echo mysql_error();				//如果不存则插入成功
    $sql = "insert into ScoreData values(NULL,$userID,'$username','$semester','$score',$courseID,'$courseName','$courseWay','$courseType',$courseScore)";
    $res = mysql_query($sql);
    if(!$res)echo mysql_error();
    else echo "$studentNum: Insert Successfully<br>";
  }
}

$sel = "select id from AverageData where userID = $userID";
$res = mysql_query($sel);
$row = mysql_fetch_assoc($res);
if($row){
  echo $row;
  echo "[Average]data is already existed<br>";
}else{

  $sql = "insert into AverageData values(NULL,$av->userID,'$av->username',{$av->data[0]},{$av->data[1]},{$av->data[2]},'',{$av->data[3]},{$av->data[4]},{$av->data[5]},{$av->data[6]},{$av->data[7]},{$av->data[8]},{$av->data[9]},{$av->data[10]},{$av->data[11]},{$av->data[12]})";

  $res = mysql_query($sql);
  if(!$res)echo mysql_error();
  else echo "$studentNum: insert sucessfully<br>";
}//for insert

if($studentNum <= 1601050150){
  $studentNum++;
  //FIX2
  echo "<script>document.location='http://yourIpAddress/StorageSZISA.php?studentNum={$studentNum}'</script>";

}


/******************************
 *         FUNCTION           *
 ******************************/
function sendPostRequest($url,$requestString,$headers,$timeout = 5){
 if($url == '' || $requestString == '' || $timeout <=0)
 return false;

 $con = curl_init((string)$url);
 curl_setopt($con, CURLOPT_HTTPHEADER, $headers);
 curl_setopt($con, CURLOPT_HEADER, false);
 curl_setopt($con, CURLOPT_POSTFIELDS, $requestString);
 curl_setopt($con, CURLOPT_POST,true);
 curl_setopt($con, CURLOPT_RETURNTRANSFER,true);
 curl_setopt($con, CURLOPT_TIMEOUT,(int)$timeout);
 return curl_exec($con); 
}

function sendGetRequest($url,$headers,$timeout = 5){
 if($url == '' || $timeout <=0)return false;

 $con = curl_init((string)$url);
 curl_setopt($con, CURLOPT_HTTPHEADER, $headers);
 curl_setopt($con, CURLOPT_HEADER, false);
 curl_setopt($con, CURLOPT_RETURNTRANSFER,true);
 #curl_setopt($con, CURLOPT_TIMEOUT,(int)$timeout);
 return curl_exec($con); 
}


?>
