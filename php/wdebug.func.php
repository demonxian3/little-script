<?php
defined('IN_IA') or exit('Access Denied');


function dump($var){
    echo '<pre>';
    var_dump($var);
    echo '</pre>';
}


function pdo_lastsql(){
    $debug = pdo_debug(0);
    $count = count($debug);
    $lastInfo = $debug[$count-1];
    $lastSql = $lastInfo['sql'];
    foreach($lastInfo['params'] as $k => $v){
        $lastSql = str_replace($k, $v, $lastSql);
    }
    echo "[sql]=><br>". $lastSql ."<br>";
    echo "[error]=><br>";
    dump($lastInfo['error']);
}


function pdo_showsql(){
    $debug = pdo_debug(0);

    foreach($debug as $val){
        $sql = $val['sql'];
        $key = $val['params'];

        foreach($key as $k => $v){
            $sql = str_replace($k, "'$v'", $sql);
        }

        echo '<div style="border:1px solid #ccc; background:#eee; padding:20px;">';
        echo $sql . "<br>";
        foreach($key as $k => $v){
            echo "[$k] => $v<br>";
        }
        echo '</div>';
    }
}

function pdo_setdata($tableName, $update, $condition){
    if(!preg_match('/cqxingyu_farm_/',$tableName))
        $tableName = 'cqxingyu_farm_' . $tableName;
    $res = pdo_update($tableName, $update, $condition);
    echo "<div style='border:1px solid #ccc;padding:20px;background:#eee'>";
    if($res){
        echo "修改成功!<br>";
    }else{
        echo "修改失败<br>";
        pdo_lastsql();
    }
    echo "</div>";
}
load()->classs("showdoc");

function showHead($filename){
    $showdoc = new ShowDoc;
    $showdoc->AutoMarkdown($filename);
}

function showFoot($result){
    $showdoc = new ShowDoc;
    error_reporting(0);
    $showdoc->AutoResult($result);
}

function showComment($tableName, $highLightArr=[]){
    $showdoc = new ShowDoc;
    $showdoc->showComment($tableName, $highLightArr);
}

function showCommentByKey($keyword=""){
    $showdoc = new ShowDoc;
    $showdoc->showCommentByKeyword($keyword);
}

function showGpcTable($arr){
    $showdoc = new ShowDoc;
    $showdoc->MkGpcTable($arr);
}

function showMdTable($arr){
    $showdoc = new ShowDoc;
    $showdoc->MdTable($arr);
}

function makeTestData(){
    $showdoc = new ShowDoc;
    $showdoc->AutoInsertData();
}

function performanceTest($begin=false){
    static $t;
    if($begin){
        $t = microtime(true);
    }else{
        echo "耗时: ".round(microtime(true)-$t, 3)."秒<br>";
        echo '耗存: '.round(memory_get_usage()/1000000,3).'M<br/>';
        $t = 0;
    }
}


?>
