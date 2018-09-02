<h3> This is XSS - referer and userAgent Test page; </h3><hr>

<?php 
   echo  " you HTTP_REFERER is : $_SERVER[HTTP_REFERER] <br>";
   echo  " you HTTP_USER_AGENT is : $_SERVER[HTTP_USER_AGENT] <br><br>";

   $borwseinfo = getBrowse();
   $addressinfo = getIP();
   $systeminfo = getOS();
  
   echo "Detecting <hr>";
   echo "Your using  borwser is $borwseinfo <br>";
   echo "Your IP address is $addressinfo <br>";
   echo "Your SystemOs is $systeminfo <br>";

//获取浏览器
function getBrowse()
{
    global $_SERVER;
    $Agent = $_SERVER['HTTP_USER_AGENT'];
    $browseinfo='';
    if(ereg('Mozilla', $Agent) && !ereg('MSIE', $Agent)){
        $browseinfo = 'Netscape Navigator';
    }
    if(ereg('Opera', $Agent)) {
        $browseinfo = 'Opera';
    }
    if(ereg('Mozilla', $Agent) && ereg('MSIE', $Agent)){

        $browseinfo = 'Internet Explorer';
    }
    if(ereg('Chrome', $Agent)){
        $browseinfo="Chrome";
    }
    if(ereg('Safari', $Agent)){
        $browseinfo="Safari";
    }
    if(ereg('Firefox', $Agent)){
        $browseinfo="Firefox";
    }

    return $browseinfo;
}
//获取ip
function getIP ()
{
    global $_SERVER;
    if (getenv('HTTP_CLIENT_IP')) {
        $ip = getenv('HTTP_CLIENT_IP');
    } else if (getenv('HTTP_X_FORWARDED_FOR')) {
        $ip = getenv('HTTP_X_FORWARDED_FOR');
    } else if (getenv('REMOTE_ADDR')) {
        $ip = getenv('REMOTE_ADDR');
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}
//获取用户系统
function getOS ()
{
    global $_SERVER;
    $agent = $_SERVER['HTTP_USER_AGENT'];
    $os = false;
    if (eregi('win', $agent) && strpos($agent, '95')){
        $os = 'Windows 95';
    }elseif (eregi('win 9x', $agent) && strpos($agent, '4.90')){
        $os = 'Windows ME';
    }elseif (eregi('win', $agent) && ereg('98', $agent)){
        $os = 'Windows 98';
    }elseif (eregi('win', $agent) && eregi('nt 5.1', $agent)){
        $os = 'Windows XP';
    }elseif (eregi('win', $agent) && eregi('nt 5.2', $agent)){    
        $os = 'Windows 2003';
    }elseif (eregi('win', $agent) && eregi('nt 5', $agent)){
        $os = 'Windows 2000';
    }elseif (eregi('win', $agent) && eregi('nt', $agent)){
        $os = 'Windows NT';
    }elseif (eregi('win', $agent) && ereg('32', $agent)){
        $os = 'Windows 32';
    }elseif (eregi('linux', $agent)){
        $os = 'Linux';
    }elseif (eregi('unix', $agent)){
        $os = 'Unix';
    }elseif (eregi('sun', $agent) && eregi('os', $agent)){
        $os = 'SunOS';
    }elseif (eregi('ibm', $agent) && eregi('os', $agent)){
        $os = 'IBM OS/2';
    }elseif (eregi('Mac', $agent) && eregi('PC', $agent)){
        $os = 'Macintosh';
    }elseif (eregi('PowerPC', $agent)){
        $os = 'PowerPC';
    }elseif (eregi('AIX', $agent)){
        $os = 'AIX';
    }elseif (eregi('HPUX', $agent)){
        $os = 'HPUX';
    }elseif (eregi('NetBSD', $agent)){
        $os = 'NetBSD';
    }elseif (eregi('BSD', $agent)){
        $os = 'BSD';
    }elseif (ereg('OSF1', $agent)){
        $os = 'OSF1';
    }elseif (ereg('IRIX', $agent)){
        $os = 'IRIX';
    }elseif (eregi('FreeBSD', $agent)){
        $os = 'FreeBSD';
    }elseif (eregi('teleport', $agent)){
        $os = 'teleport';
    }elseif (eregi('flashget', $agent)){
        $os = 'flashget';
    }elseif (eregi('webzip', $agent)){
        $os = 'webzip';
    }elseif (eregi('offline', $agent)){
        $os = 'offline';
    }else{
        $os = 'Unknown';
    }
    return $os;
}
   
?>
