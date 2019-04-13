<?php
    $database = 'applet_mobile';
    $con = mysqli_connect("localhost","root","xfdada") or die("cannot connect mysql");
    mysqli_set_charset($con,"utf8");
    $tableSql = "select * from information_schema.tables where table_schema = '$database'";
    $tableRes = mysqli_query($con, $tableSql) or die(mysqli_error($con));
    while($tableRow = mysqli_fetch_assoc($tableRes)){
        if($tableRow['TABLE_COMMENT']) $tableCom = $tableRow['TABLE_COMMENT'];
        $tableName = $tableRow['TABLE_NAME'];
        echo "** $tableName ($tableCom) **<br><br>";

        $columnSql = "select * from information_schema.columns where table_name = '$tableName'";
        $columnRes = mysqli_query($con, $columnSql) or die(mysqli_error($con));

        echo "|字段名|字段类型|扩展|是否为空|键值|注释|<br>";
        echo "|------|----|---|---|---|---|<br>";
        while($columnRow = mysqli_fetch_assoc($columnRes)){
        echo "|$columnRow[COLUMN_NAME]|$columnRow[COLUMN_TYPE]|$columnRow[EXTRA]|$columnRow[IS_NULLABLE]|$columnRow[COLUMN_KEY]|$columnRow[COLUMN_COMMENT]|<br>";
        }

        echo "<br><br>";
    }
?>
