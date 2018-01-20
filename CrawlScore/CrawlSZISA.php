<?php
# @Auth: Demon
# @Date: 2018-1-20
# @Vers: 1.0
# @Desc: Crawl the score of student from SZISA;

extract($_GET);

/* CHECK FUNCTION  */      		#if php version<5.4 , define function:gzdecode
if(!function_exists('gzdecode')){
  function gzdecode($data){
    return gzinflate(substr($data,10,-8));
  }
}

$studentNum = 1601050112;

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


foreach($res->result as $title => $value){
  if(preg_match("/学期/",$title)){
    $scores->semester = $title;

    if(!isset($queryName)){
        $queryName = $value[0]->username;		//姓名
	echo $queryName.":".$studentNum."<br><br>"; 
    }
    if(!isset($queryID)) $queryID = $value[0]->userid;		//学号

    echo $title."<br><table border='1'>";
    foreach($value as $item){
      echo "<tr>
            <td style='width:200px'>$item->course_name</td>
            <td style='width:60px'>$item->total</td>
            <td style='width:80px'>$item->course_type</td>
            <td style='width:60px'>$item->method</td>
            <td style='width:40px'>$item->credit</td>
            <td style='width:90px'>$item->course_code</td>
            <tr>";
    }

    echo "</table>";
  }
  
  else if(preg_match("/^平均分$/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
     }
  }

  else if(preg_match("/学年/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
     }
  }

  else if(preg_match("/总评/",$title)){
     echo "<h4>$title</h4>";
     foreach($value as $key => $score){
       echo "$key: $score<br>";
     }
  }
  
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
 curl_setopt($con, CURLOPT_TIMEOUT,(int)$timeout);
 return curl_exec($con); 
}


?>
