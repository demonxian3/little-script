#!/bin/bash
#version: 2.2
#author:  Khazix Li
#date:    2019/05/07

#config
version="2.0"                   #shell version
username=root                   #username
password=root                   #password
database=mysql                  #default database
host="localhost"                #default host
table=""                        #default table
where="1=1"                     #default where condition
column="*"                      #default column
tableChar="utf-8"               #default Character set for creating table
tableEngine="InnoDb"            #default engine for creating table


#error code
NOR_MSG_SHOWSQL=101
NOR_MSG_SHOWRES=102
NOR_MSG_SHOWVAR=103
WAR_OPR_CONFIRM=301
WAR_OPT_INVALID=302
ERR_ACT_INVALID=501
ERR_OPT_REQUIRE=502
ERR_VAL_REQUIRE=503

function help(){

if [[ -n $a ]];then
    case $a in 
        'sr')      echo "select \$c from \$d.\$t [where \$w]"; ;;
        'ir')      echo "insert into \$d.\$t(\$c) values(\$v)"; ;;
        'ur')      echo "update \$d.\$t set (\$v) [where \$w]"; ;;
        'dr')      echo "delete from \$d.\$t [where \$w]"; ;;
        'st')      echo "show tables"; ;;
        'dt')      echo "drop table \$d.\$t"; ;;
        'ct')      echo "create table \$d.\$t(\$c)"; ;;
        'sct')     echo "show create table \$d.\$t"; ;;
        'dst')     echo "desc \$d.\$t"; ;;
        'sd')      echo "show databases"; ;;
        'cd')      echo "create database \$d"; ;;
        'dd')      echo "drop database \$d"; ;;
        'cc')      echo "select from infor where tname = \$d.\$t"; ;;
        'sv')      echo "show variables like '%\$v%'"; ;;
        'su')      echo "select \$c from mysql.user where \$w" ;;
        'cu')      echo "create user \$u identified by password '\$v'" ;;
        'du')      echo "drop user \$u" ;;
        'gu')      echo "grant \$v on \$d.\$t to \$u" ;;
        'sg')      echo "show grants for \$u";;
        'up')      echo "mysqladmin \$v"; ;;
        'sql')     echo "execute \$v;"; ;;
        'into')    echo "into interact shell"; ;;
        'bak')     echo "mysqldump \$d"; ;;
        'src')     echo "source \$v"; ;;
        'ver')     echo "select version();"; ;;
    esac
    exit;
fi

    cat <<EOF
Usage: db [OPTION]... 
  -u,  --user                specify user@host
  -c,  --column              specify column
  -t,  --table               specify table 
  -d,  --database            specify database
  -v,  --value               specify value
  -f,  --field               select the field on cut command
  -g,  --format              format output the execution result,
                             actually equivalent to adding '\\G' in 
                             the end of SQL 
  -y,  --yes                 data write operation needs to be confirm
                             use -y say yes, do it.
  -w,  --where               specify condition for SQL operation
  -h,  --help                use -a option get help for action
  -a,  --action              record action: sr,ir,ur,dr
                             table action: st,dt,ct,dst,sct
                             database action: sd,cd,dd
                             column action: cc
                             variables: sv
                             mysql function: sql,into,src,bak
                             show shell variables: .v .u .d
EOF
    exit;
}

function showMessage(){
    case $1 in
    101)echo "$2";;    #[SQL:101] 
    102)echo "$2";;    #[RES:102] 
    103)echo "$2";;    #[VAR:103] 
    301)echo "[WAR:301] confirm operation, use -y make sure to do it"; noConfirm=1; ;;
    302)echo "[WAR:302] $2 is invalid option.";                                     ;;
    501)echo "[ERR:501] Invalid action\n";showActionList;exit          ;;
    502)echo "[ERR:502] $2 option is required"; exit;                               ;;
    503)
        echo "[ERR:503] option $2 need specify a value, use -h for help";
        if [[ $2 -eq '-a' ]];then showActionList;fi;
        exit;
    ;;
    esac
}

function showActionList(){
    echo '[st|dt|ct|dst|sct]'
    echo '[sr|dr|ur|ir] '
    echo '[sd|dd|cd|cc|sv]'
    echo '[sql|bak|src|into]'
    echo '[cu|du|up|gu|sg|su]'
    echo '[.v|.u|.d]'
}

function checkOption(){
    while [[ -n "$1" ]];do
        case $1 in 
            '-a') if [[ -z $a ]];then showMessage $ERR_OPT_REQUIRE '-a'; fi; ;;
            '-d') if [[ -z $d ]];then showMessage $ERR_OPT_REQUIRE '-d'; fi; ;;
            '-t') if [[ -z $t ]];then showMessage $ERR_OPT_REQUIRE '-t'; fi; ;;
            '-c') if [[ -z $c ]];then showMessage $ERR_OPT_REQUIRE '-c'; fi; ;;
            '-w') if [[ -z $w ]];then showMessage $ERR_OPT_REQUIRE '-w'; fi; ;;
            '-v') if [[ -z $v ]];then showMessage $ERR_OPT_REQUIRE '-v'; fi; ;;
            '-u') if [[ -z $u ]];then showMessage $ERR_OPT_REQUIRE '-u'; fi; ;;
            '-y') if [[ -z $y ]];then showMessage $WAR_OPR_CONFIRM '-y'; fi; ;;
        esac
        shift;
    done
}

function setIfDefault(){
    while [[ -n "$1" ]];do
        case $1 in 
            '-d') if [[ -z $d ]];then d="$database";else d="$d" ;fi; ;;
            '-t') if [[ -z $t ]];then t="$table"   ;else t="$t" ;fi; ;;
            '-c') if [[ -z $c ]];then c="$column"  ;else c="$c" ;fi; ;;
            '-w') if [[ -z $w ]];then w="$where"   ;else w="$w" ;fi; ;;
            '-u') if [[ -z $u ]];then u="$username@$host"   ;else u="$u" ;fi; ;;
        esac
        shift;
    done
}

if [[ -z $1 ]];then help; fi 

while [[ -n "$1" ]];do
    case $1 in
        "-u")  if [[ -n "$2" ]]; then u=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-u'; fi ;;
        "-a")  if [[ -n "$2" ]]; then a=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-a'; fi ;;
        "-d")  if [[ -n "$2" ]]; then d=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-d'; fi ;;
        "-t")  if [[ -n "$2" ]]; then t=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-t'; fi ;;
        "-c")  if [[ -n "$2" ]]; then c=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-c'; fi ;;
        "-v")  if [[ -n "$2" ]]; then v=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-v'; fi ;;
        "-f")  if [[ -n "$2" ]]; then f=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-f'; fi ;;
        "-w")  if [[ -n "$2" ]]; then w=$2;shift 2; else showMessage $ERR_VAL_REQUIRE '-w'; fi ;;
        "-g")  g=1 ;         shift 1;;
        "-y")  y=1 ;         shift 1;;
        "-h")  help;         shift 1;;
        *) showMessage $WAR_OPT_INVALID $1; shift 1;;
    esac
done

checkOption '-a';

case $a in
    "sr")
        checkOption '-t';
        setIfDefault '-c' '-w' '-d';
        sql="select $c from $d.$t where $w"
        ;;
    "ir")
        checkOption '-t' '-v' '-y';
        setIfDefault '-d';
        sql="insert into $d.$t($c) values($v);"
        ;;
    "ur")
        checkOption '-t' '-v' '-y';
        setIfDefault '-d' '-w';
        sql="update $d.$t set $v where $w";
        ;;
    "dr")
        checkOption '-t' '-w' '-y';
        setIfDefault '-d'
        sql="delete from $d.$t where $w;";
    ;;
    "dt")
        checkOption '-t' '-y';
        setIfDefault '-d';
        sql="drop table $d.$t;";
    ;;
    "ct")
        checkOption '-t' '-c' '-y';
        setIfDefault '-d';
        sql="create table $d.$t ($c)";
    ;;
    "st")
        setIfDefault '-d';
        sql="use $d;show tables;";
    ;;
    "dst")
        checkOption '-t';
        setIfDefault '-d';
        sql="desc $d.$t";
    ;;
    "sct")
        checkOption '-t';
        setIfDefault '-d';
        sql="show create table $d.$t";
    ;;
    "sd")
        sql="show databases;";
    ;;
    "cd")
        checkOption '-d';
        sql="create database $d;";
    ;;
    "dd")
        checkOption '-d' '-y';
        sql="drop database $d;";
    ;;
    "cc")
        checkOption '-t';
        sql="select distinct 
            ORDINAL_POSITION, COLUMN_NAME,
            IS_NULLABLE, COLUMN_TYPE,
            COLUMN_DEFAULT, EXTRA,
            COLUMN_KEY, COLUMN_COMMENT 
            from information_schema.columns 
            where table_name = '$t'";
    ;;
    "sv")
         sql="show variables like '%$v%'";
    ;;
    "into")
        mysql -u$username -p$password -A;exit;
    ;;
    "bak")
        checkOption '-d';
        mysqldump -u$username -p$password $d > $d-$(date +%Y%m%d).sql
        exit;
    ;;
    "su")
        setIfDefault '-w' '-c';
        sql="select $c from mysql.user where $w";
    ;;
    "cu")
        checkOption '-u' '-v' '-y';
        sql="create user $u identified by '$v'";
    ;;
    "du")
        checkOption '-u' '-y';
        sql="drop user $u ";
    ;;
    "gu")
        checkOption '-u' '-y' '-v' '-t' '-d';
        sql="grant $v on $d.$t to $u;flush privileges;";
    ;;
    "sg")
        checkOption '-u';
        sql="show grants for $u";
    ;;
    "up")
        checkOption '-v';
        mysqladmin -u$username -p$password password $v;
        if [[ $? -eq 0 ]];then sed -i "s/$password/$v/g" $0; fi;
        exit;
    ;;
    "src")
        checkOption '-d' '-v' '-y';
        sql="use $d;source $v;"
    ;;
    "sql")
        checkOption '-d' '-v' '-y';
        sql="$v";
    ;;
    ".v")
        showMessage $NOR_MSG_SHOWVAR $version
    ;;
    ".u")
        showMessage $NOR_MSG_SHOWVAR "$username  $password"
    ;;
    ".d")
        showMessage $NOR_MSG_SHOWVAR $database
    ;;
    *)
        showMessage $ERR_ACT_INVALID $a;
    ;;
esac


#display
echo  "$sql"


#confirm
if [[ $noConfirm -eq 1 ]];then exit; fi;

#format
if [[ $g == "1" ]];then sql="$sql\\G"; fi

result=$(echo "$sql" | mysql -u"$username" -p"$password" -A);

#output
result="${result//\`/}"
if [[ $f ]];then
    echo "$result" | cut -f $f | column -t;
else
    echo "$result" | column -t;
fi
