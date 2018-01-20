<?php
# @Auth: Demon
# @Date: 2018-1-20
# @Vers: 2.1
# @Desc: Crawl the score of student from Shenxin;

extract($_GET);

/* CHECK FUNCTION  */      		#if php version<5.4 , define function:gzdecode
if(!function_exists('gzdecode')){
  function gzdecode($data){
    return gzinflate(substr($data,10,-8));
  }
}

if(!isset($startNum))$startNum = 1601050114;
if(!isset($stopNum))$stopNum = 1601050117;

//swap the stopNum and startNum
if($stopNum < $startNum){
  $startNum -= $stopNum;		//  7 - 4 = 3 startNum
  $stopNum += $startNum;		//  4 + 3 = 7 stopNum
  $startNum = $stopNum - $startNum;     //  7 - 3 = 4 startNum 
}

for($studentNum=$startNum; $studentNum<=$stopNum; $studentNum++){

/* FORGE HEADER */
$Headers = array();
$Headers[] = "Host: lihailewordge.shenxin.ren";
$Headers[] = "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0";
$Headers[] = "Accept: application/json, text/javascript, */*; q=0.01";
$Headers[] = "Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2";
$Headers[] = "Accept-Encoding: gzip, deflate";
$Headers[] = "Referer: http://lihailewordge.shenxin.ren/home/queryscore?number=1608070130&from=singlemessagehttp://lihailewordge.shenxin.ren/home/queryscore?number=1608070130&from=singlemessage";
$Headers[] = "Content-Type: application/x-www-form-urlencoded; charset=UTF-8";
$Headers[] = "Auth-Token: 9ZB2pmCmpMuowN4mCvCiX7gBDNkTmeQxNXKqgn9i8OYHeha6Op";
$Headers[] = "X-Requested-With: XMLHttpRequest";
$Headers[] = "Content-Length: 77";
$Headers[] = "Cookie: ci_session=8a3d0bb61e0b93b1c1aed12b5af03f0ffe01ed87";
$Headers[] = "Connection: keep-alive";
$Headers[] = "Cache-Control: max-age=0";
$TargetUrl = "http://lihailewordge.shenxin.ren/api/getScore";
$PostData  = "number={$studentNum}&viewcode=9ZB2pmCmpMuowN4mCvCiX7gBDNkTmeQxNXKqgn9i8OYHeha6Op";

/*  Main Function */
$Response = sendPostRequest($TargetUrl,$PostData,$Headers);
$ExtractData = gzdecode($Response);
$res = json_decode($ExtractData);

$average= Array();
$nums = $res->result->score[0]->list[0]->number;
$name = $res->result->queryname;
$tips = $res->result->buttomtips;
$aver = $res->result->avglist;
$core = $res->result->score;

//存储学期平均分
foreach($aver as $obj){
  $average["{$obj->score}"] = "{$obj->year}学年 第{$obj->term}学期";
}

echo "姓名： $name<br>";
echo "学号： $nums<br>";

foreach($core as $term){
  echo "<table border='1'>";
  echo "<tr><td colspan='4'><center>$term->title<center></td></tr>";
  #echo "<div style='width:600px;border:2px solid #c3c3c3'></div>";
  foreach($term->list as $data){
    echo "<tr>
	<td style='width:300px'>$data->lesson</td>
	<td style='width:60px'>$data->ksScore</td>
	<td style='width:75px'>$data->way</td>
	<td>$data->lstype</td>
	</tr>";
  }
  echo "</table>";
  

  foreach($average as $key => $value)
    if($value == $term->title)echo "学期平均分： $key<br><br>";
}


preg_match('/(\d+\.\d*).*?(\d+\.\d*).*?(\d+\.?\d*)/',$tips,$matches);
echo "平均分：" . $matches[1] ."<br>";
echo "通过分：" . $matches[2] ."<br>";
echo "未过分：" . $matches[3] ."<br>";

echo "##############################################################<br>";

}  //for

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


?>
