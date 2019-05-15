#!/bin/bash
#version: 2.5
#author:  Khazix Li
#date:    2019/05/07

#config
version="2.5"                   #shell version
username=root                   
password=root       
database=mysql       
host="localhost"                #default host
table=""                        #default table
where="1=1"                     #default where condition
column="*"                      #default column
tbChar="utf8"                   #default character set for creating table: [latin1], [utf8] [gbk]
tbEngine="InnoDB"               #default engine for creating table: [InnoDB], [MYISAM], [Memory]
dbChar="utf8"                   #default character set for creating database: [latin1], [utf8] [gbk]
dbCollate="utf8_general_ci"     #default collate: [utf8_general_ci] [gbk_chinese_ci] 

#global variables
d="";
t="";
c="";
w="";
u="";
v="";
sql="";
res="";
errno=0;

#color variables
ccls="\033[00m"
fred="\033[31m"
fvio="\033[32m"
fyel="\033[33m"
fblu="\033[34m"
fpin="\033[35m"
fyan="\033[36m"
fgra="\033[37m"
bbla="\033[40m"
bred="\033[41m"
bvio="\033[42m"
byel="\033[43m"
bblu="\033[44m"
bpin="\033[45m"
byan="\033[46m"
bgra="\033[47m"

#error variables
NOR_PUTMSG=100
NOR_PUTVAR=101
NOR_PUTSQL=102
NOR_PUTRES=103
NOR_PUTEND=109
WAR_OPRCFM=301
WAR_OPTIVL=302
ERR_ACTIVL=501
ERR_OPTREQ=502
ERR_VALREQ=503


function help(){
#ACT
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
        'up')      echo "set password for \$u = password('\$v')"; ;;
        'sql')     echo "mysql> \$v;"; ;;
        'into')    echo "into interact shell"; ;;
        'bak')     echo "mysqldump \$d"; ;;
        'chp')     echo "mysqladmin -u\$usr -p\$pwd \$v \$d"; ;;
        'src')     echo "source \$v"; ;;
        'ver')     echo "select version();"; ;;
    esac
    exit;
fi

#OPT
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

function putActLst(){
    #ACT
    echo -e $fyan;
    echo '[action list]:'
    echo '[table]    st dt ct cc dst sct '
    echo '[record]   sr dr ur ir  '
    echo '[database] sd dd cd sv '
    echo '[function] sql bak src into chp '
    echo '[user]     cu du up gu sg su up '
    echo '[shell]    .v .u .d '
    echo -e $ccls;
}


function putMsg(){
    case $errno in
    $NOR_PUTMSG)  echo $2; ;;
    $NOR_PUTEND)  echo -e $ccls; ;;
    $NOR_PUTVAR)  echo -e "$bbla[VAR:$errno]$ccls$2"; ;;
    $NOR_PUTSQL)  echo -e "$bblu[SQL:$errno]$ccls$fblu$sql$ccls"; ;;
    #$NOR_PUTRES)  echo -e "$bvio[RES:$errno]$ccls\n$fvio$res$ccls"; ;;
    $NOR_PUTRES)  echo -e "$bvio[RES:$errno]$ccls\n$fvio"; ;;
    $WAR_OPRCFM)  echo -e "$byel[WAR:$errno]$ccls$fyel use -y make sure to do it$ccls"; noConfirm=1; ;;
    $WAR_OPTIVL)  echo -e "$byel[WAR:$errno]$ccls$fyel -$1 is invalid option.";                 $ccls ;;
    $ERR_ACTIVL)  echo -e "$bred[ERR:$errno]$ccls$fred Invalid action$ccls";putActLst;exit      $ccls ;;
    $ERR_OPTREQ)  echo -e "$bred[ERR:$errno]$ccls$fred -$1 option is required$ccls"; exit;      $ccls ;;
    $ERR_VALREQ)  echo -e "$bred[ERR:$errno]$ccls$fred option -$1 need specify a value$ccls"    $ccls;
                  if [[ $1 -eq '-a' ]];then putActLst;fi;
                  exit;
    ;;
    esac
}

function chkOpt(){
    #OPT
    while [[ -n "$1" ]];do
        case $1 in 
            'a') if [[ -z $a ]];then errno=$ERR_OPTREQ;putMsg a; fi; ;;
            'd') if [[ -z $d ]];then errno=$ERR_OPTREQ;putMsg d; fi; ;;
            't') if [[ -z $t ]];then errno=$ERR_OPTREQ;putMsg t; fi; ;;
            'c') if [[ -z $c ]];then errno=$ERR_OPTREQ;putMsg c; fi; ;;
            'w') if [[ -z $w ]];then errno=$ERR_OPTREQ;putMsg w; fi; ;;
            'v') if [[ -z $v ]];then errno=$ERR_OPTREQ;putMsg v; fi; ;;
            'u') if [[ -z $u ]];then errno=$ERR_OPTREQ;putMsg u; fi; ;;
            'y') if [[ -z $y ]];then errno=$WAR_OPRCFM;putMsg y; fi; ;;
        esac
        shift;
    done
}

function setDef(){
    #OPT
    while [[ -n "$1" ]];do
        case $1 in 
            'd') if [[ -z $d ]];then d="$database";else d="$d" ;fi; ;;
            't') if [[ -z $t ]];then t="$table"   ;else t="$t" ;fi; ;;
            'c') if [[ -z $c ]];then c="$column"  ;else c="$c" ;fi; ;;
            'w') if [[ -z $w ]];then w="$where"   ;else w="$w" ;fi; ;;
            'u') if [[ -z $u ]];then u="$username@$host"   ;else u="$u" ;fi; ;;
        esac
        shift;
    done
}

function setSql(){
    #ACT
    case $a in 
    'sr') sql="SELECT $c FROM $d.$t WHERE $w"
     ;;
    'ir') sql="INSERT INTO $d.$t($c) VALUES($v)"
     ;;
    'ur') sql="UPDATE $d.$t SET $v WHERE $w";     
     ;;
    'dr') sql="DELETE FROM $d.$t WHERE $w;";      
     ;;
    'dt') sql="DROP TABLE $d.$t;";                
     ;;
    'ct') sql="CREATE TABLE $d.$t ($c)ENGINE=$tbEngine DEFAULT CHARSET=$tbChar";                                
     ;;
    'st') sql="USE $d;SHOW TABLES;";              
     ;;
    'dst')sql="DESC $d.$t";                       
     ;;
    'sct')sql="SHOW CREATE TABLE $d.$t";          
     ;;
    'sd') sql="SHOW DATABASES;";                  
     ;;
    'cd') sql="CREATE DATABASE $d DEFAULT CHARACTER SET '$dbChar' COLLATE '$dbCollate'";   
     ;;
    'dd') sql="DROP DATABASE $d;";                
     ;;
    'cc') sql="SELECT DISTINCT ordinal_position,column_name,is_nullable,column_type,column_default,extra,column_key,column_comment FROM information_schema.columns WHERE table_name='$t'";                 
     ;;
    'sv') sql="SHOW VARIABLES LIKE '%$v%'";         
     ;;
    'su') sql="SELECT $c FROM mysql.user WHERE $w"; 
     ;;
    'cu') sql="CREATE USER $u IDENTIFIED BY '$v'";  
     ;;
    'du') sql="DROP USER $u ";                      
     ;;
    'gu') sql="GRANT $v ON $d.$t TO $u;FLUSH PRIVILEGES;"; 
     ;;
    'sg') sql="SHOW GRANTS FOR $u";                 
     ;;
    'up') sql="SET PASSWORD FOR $u = password('$v')";
     ;;
    'src')sql="USE $d;SOURCE $v";
     ;;
    'sql')sql="$sql";
     ;;

    esac;
}




# /*   MAIN   */
if [[ -z $1 ]];then help; fi 
while [[ -n "$1" ]];do
    #OPT
    case $1 in
        "-u")  if [[ -n "$2" ]]; then u=$2;shift 2; else errno=$ERR_VALREQ;putMsg u; fi ;;
        "-a")  if [[ -n "$2" ]]; then a=$2;shift 2; else errno=$ERR_VALREQ;putMsg a; fi ;;
        "-d")  if [[ -n "$2" ]]; then d=$2;shift 2; else errno=$ERR_VALREQ;putMsg d; fi ;;
        "-t")  if [[ -n "$2" ]]; then t=$2;shift 2; else errno=$ERR_VALREQ;putMsg t; fi ;;
        "-c")  if [[ -n "$2" ]]; then c=$2;shift 2; else errno=$ERR_VALREQ;putMsg c; fi ;;
        "-v")  if [[ -n "$2" ]]; then v=$2;shift 2; else errno=$ERR_VALREQ;putMsg v; fi ;;
        "-f")  if [[ -n "$2" ]]; then f=$2;shift 2; else errno=$ERR_VALREQ;putMsg f; fi ;;
        "-w")  if [[ -n "$2" ]]; then w=$2;shift 2; else errno=$ERR_VALREQ;putMsg w; fi ;;
        "-g")  g=1 ;         shift 1;;
        "-y")  y=1 ;         shift 1;;
        "-h")  help;         shift 1;;
        "-st"|"-dt"|"-ct"|"-dst"|"-sct"|"-sr"|"-dr"|"-ur"|"-ir"|"-sd"|"-dd"|"-cd"|"-cc"|"-sv"|"-sql"|"-bak"|"-src"|"-into"|"-cu"|"-du"|"-up"|"-gu"|"-sg"|"-su"|"-chp")
        a="${1:1}"; shift 1;;
        *) errno=$WAR_OPTIVL; putMsg $1; shift 1;;
    esac
done


chkOpt '-a';

#ACT
case $a in
    "sr")
        chkOpt t;
        setDef c w d;
        ;;
    "ir")
        chkOpt t v y;
        setDef d;
        ;;
    "ur")
        chkOpt t v w y;
        setDef d;
        ;;
    "dr")
        chkOpt t w y;
        setDef d;
    ;;
    "dt")
        chkOpt t y;
        setDef d;
    ;;
    "ct")
        chkOpt t c y;
        setDef d;
    ;;
    "st")
        setDef d;
    ;;
    "dst")
        chkOpt t;
        setDef d;
    ;;
    "sct")
        chkOpt t;
        setDef d;
    ;;
    "sd")
    ;;
    "cd")
        chkOpt d;
    ;;
    "dd")
        chkOpt d y;
    ;;
    "cc")
        chkOpt t;
    ;;
    "sv")
    ;;
    "su")
        setDef w c;
    ;;
    "cu")
        chkOpt u v y;
    ;;
    "du")
        chkOpt u y;
    ;;
    "gu")
        chkOpt u v t d y;
    ;;
    "sg")
        chkOpt u;
    ;;
    "up")
        chkOpt u v y;
    ;;
    "into")
        mysql -u$username -p$password -A;
        exit;
    ;;
    "bak")
        chkOpt d;
        mysqldump -u$username -p$password $d > $d-$(date +%Y%m%d).sql
        exit;
    ;;
    "chp")
        chkOpt v;
        mysqladmin -u$username -p$password password $v;
        if [[ $? -eq 0 ]];then sed -i "s/$password/$v/g" $0; fi;
        exit;
    ;;
    "src")
        chkOpt d v y;
    ;;
    "sql")
        chkOpt d v y;
    ;;
    ".v")
        errno=$NOR_PUTVAR;
        putMsg $version
    ;;
    ".u")
        errno=$NOR_PUTVAR;
        putMsg "$username  $password"
    ;;
    ".d")
        errno=$NOR_PUTVAR;
        putMsg $database
    ;;
    *)
        errno=$ERR_ACTIVL;
        putMsg $a;
    ;;
esac

#showsql
setSql;
errno=$NOR_PUTSQL;
putMsg;


#confirm
if [[ $noConfirm -eq 1 ]];then exit; fi;

#format
if [[ $g == "1" ]];then sql="$sql\\G"; fi


#output
errno=$NOR_PUTRES;
putMsg;
res=$(echo "$sql" | mysql -u"$username" -p"$password" -A);
res="${res//\`/}"
if [[ $f ]];then
    #echo "$res" | cut -f $f | column -t;
    echo "$res" | cut -f $f
else
    echo "$res"
    #echo "$res" | column -t;
fi
errno=$NOR_PUTEND;
putMsg;
