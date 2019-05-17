#!/bin/bash
#version: 4.0
#author:  Khazix Li
#date:    2019/05/17

#config
version="4.0"                   #shell version
username=root                   
password=30caa3216fbb4bac       
database=newzhnc_xyqkl_cn       
host="localhost"                #default host
table="user"                    #default table
where="1=1"                     #default where condition
column="*"                      #default column
tbChar="utf8"                   #default character set for creating table: [latin1], [utf8] [gbk]
tbEngine="InnoDB"               #default engine for creating table: [InnoDB], [MYISAM], [Memory]
dbChar="utf8"                   #default character set for creating database: [latin1], [utf8] [gbk]
dbCollate="utf8_general_ci"     #default collate: [utf8_general_ci] [gbk_chinese_ci] 

dbCacheFile="/tmp/db.tmp"
tbCacheFile="/tmp/tb.tmp"

#global variables
d="";
t="";
c="";
w="";
u="";
v="";
sql="";
res="";
db_arr="";
tb_arr="";

#color variables
ccls="\033[00m"
fred="\033[31m"
fvio="\033[32m"
fyel="\033[33m"
fblu="\033[34m"
fpin="\033[35m"
fyan="\033[36m"
fgra="\033[37m"
bbla="\033[40;37;1m"
bred="\033[41;37;1m"
bvio="\033[42;37;1m"
byel="\033[43;37;1m"
bblu="\033[44;37;1m"
bpin="\033[45;37;1m"
byan="\033[46;37;1m"
bgra="\033[47;37;1m"

#error variables
NOR_PUTMSG=100
NOR_PUTVAR=101
NOR_PUTSQL=102
NOR_PUTRES=103
NOR_HITDBN=104
NOR_HITTBN=105
WAR_OPRCFM=301
WAR_OPTIVL=302
WAR_CACNUL=303
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
        'sel')     echo "into interact shell"; ;;
        'bak')     echo "mysqldump \$d"; ;;
        'chp')     echo "mysqladmin -u\$usr -p\$pwd \$v \$d"; ;;
        'src')     echo "source \$v"; ;;
        'ver')     echo "select version();"; ;;
        *)         putActLst; ;;
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
                             mysql function: sql,shl,src,bak
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
    echo '[function] sql bak src shl chp ver '
    echo '[user]     cu du up gu sg su up '
    echo '[shell]    .v .u .d '
    echo -e $ccls;
}


function putMsg(){
    case $1 in
    $NOR_PUTMSG)  echo $2; ;;
    $NOR_PUTVAR)  echo -e "$bbla[NOR_PUTVAR]$ccls$fbla$2$ccls";   exit;;
    $NOR_PUTSQL)  echo -e "$bblu[NOR_PUTSQL]$ccls\n$fblu$2$ccls"; ;;
    $NOR_PUTRES)  echo -e "$bvio[NOR_PUTRES]$ccls\n$fvio$2";      ;;
    $NOR_HITTBN)  echo -e "$bpin[CUR_TABLEN]$ccls$fpin$2$ccls";   ;;
    $NOR_HITDBN)  echo -e "$byan[CUR_DBNAME]$ccls$fyan$2$ccls";   ;;
    $WAR_OPRCFM)  echo -e "$byel[WAR_OPRCFM]$ccls$fyel use -y make sure to do it$ccls"; noConfirm=1; ;;
    $WAR_OPTIVL)  echo -e "$byel[WAR_OPTIVL]$ccls$fyel -$2 is invalid option.$ccls";            ;;
    $WAR_CACNUL)  echo -e "$byel[WAR_OPTIVL]$ccls$fyel $2 isn't hit in cache.$ccls";            ;;
    $ERR_ACTIVL)  echo -e "$bred[ERR_ACTIVL]$ccls$fred Invalid action$ccls";putActLst;exit      ;;
    $ERR_OPTREQ)  echo -e "$bred[ERR_OPTREQ]$ccls$fred -$2 option is required$ccls"; exit;      ;;
    $ERR_VALREQ)  echo -e "$bred[ERR_VALREQ]$ccls$fred option -$2 need specify a value$ccls"    ;
                  if [[ $2 -eq '-a' ]];then putActLst;fi;
                  exit;
    ;;
    esac
}

function chkOpt(){
    #OPT
    while [[ -n "$1" ]];do
        case $1 in 
            'a') if [[ -z $a ]];then putMsg $ERR_OPTREQ a; fi; ;;
            'd') if [[ -z $d ]];then putMsg $ERR_OPTREQ d; fi; ;;
            't') if [[ -z $t ]];then putMsg $ERR_OPTREQ t; fi; ;;
            'c') if [[ -z $c ]];then putMsg $ERR_OPTREQ c; fi; ;;
            'w') if [[ -z $w ]];then putMsg $ERR_OPTREQ w; fi; ;;
            'v') if [[ -z $v ]];then putMsg $ERR_OPTREQ v; fi; ;;
            'u') if [[ -z $u ]];then putMsg $ERR_OPTREQ u; fi; ;;
            'y') if [[ -z $y ]];then putMsg $WAR_OPRCFM y; fi; ;;
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
    'ver')sql="SELECT @@version";
     ;;
    'sql')sql="$sql";
     ;;

    esac;
}

function setDbn(){
    if [[ -e $dbCacheFile && $1 -gt 0 ]] 2>/dev/null; then
        d=`sed -n "${1}p" $dbCacheFile`;
        if [[ -z $d ]];then
            putMsg $WAR_CACNUL database;
            d=$database;
        fi
    else
        d=$1;
    fi
}

function setTbn(){
    if [[ -e $tbCacheFile && $1 -gt 0 ]] 2>/dev/null; then
        t=`sed -n "${1}p" $tbCacheFile`;
        if [[ -z $t ]];then
            putMsg $WAR_CACNUL table;
            t=$table;
        fi
    else
        t=$1;
    fi
}

# /*   MAIN   */
if [[ -z $1 ]];then help; fi 
while [[ -n "$1" ]];do
    #OPT
    case $1 in
        "-d")  if [[ -n "$2" ]]; then setDbn $2;shift 2; else a="sd"; shift 1; fi ;;
        "-t")  if [[ -n "$2" ]]; then setTbn $2;shift 2; else a="st"; shift 1; fi ;;
        "-u")  if [[ -n "$2" ]]; then u=$2;shift 2; else putMsg $ERR_VALREQ u; fi ;;
        "-a")  if [[ -n "$2" ]]; then a=$2;shift 2; else putMsg $ERR_VALREQ a; fi ;;
        "-c")  if [[ -n "$2" ]]; then c=$2;shift 2; else putMsg $ERR_VALREQ c; fi ;;
        "-v")  if [[ -n "$2" ]]; then v=$2;shift 2; else putMsg $ERR_VALREQ v; fi ;;
        "-f")  if [[ -n "$2" ]]; then f=$2;shift 2; else putMsg $ERR_VALREQ f; fi ;;
        "-w")  if [[ -n "$2" ]]; then w=$2;shift 2; else putMsg $ERR_VALREQ w; fi ;;
        "-g")  g=1 ;         shift 1;;
        "-y")  y=1 ;         shift 1;;
        "-h")  help;         shift 1;;
        "-st"|"-dt"|"-ct"|"-dst"|"-sct"|"-sr"|"-dr"|"-ur"|"-ir"|"-sd"|"-dd"|"-cd"|"-cc"|"-sv"|"-sql"|"-bak"|"-src"|"-shl"|"-cu"|"-du"|"-up"|"-gu"|"-sg"|"-su"|"-chp"|"-ver")
        a="${1:1}"; shift 1;;
        *)  putMsg $WAR_OPTIVL $1; shift 1;;
    esac
done

chkOpt '-a';

#ACT
case $a in
    "sr")  chkOpt t;       setDef c w d;   ;;
    "ir")  chkOpt t v y;   setDef d;       ;;
    "ur")  chkOpt t v w y; setDef d;       ;;
    "dr")  chkOpt t w y;   setDef d;       ;;
    "dt")  chkOpt t y;     setDef d;       ;;
    "ct")  chkOpt t c y;   setDef d;       ;;
    "st")  setDef d;       ;;
    "dst") chkOpt t;       setDef d;       ;;
    "sct") chkOpt t;       setDef d;       ;;
    "sd")  ;;
    "cd")  chkOpt d;         ;;
    "dd")  chkOpt d y;       ;;
    "cc")  chkOpt t;         ;;
    "sv")  ;;
    "su")  setDef w c;       ;;
    "cu")  chkOpt u v y;     ;;
    "du")  chkOpt u y;       ;;
    "gu")  chkOpt u v t d y; ;;
    "sg")  chkOpt u;         ;;
    "up")  chkOpt u v y;     ;;
    "shl") mysql -u$username -p$password -A; exit; ;;
    "bak") chkOpt d; mysqldump -u$username -p$password $d > $d-$(date +%Y%m%d).sql exit; ;;
    "src") chkOpt d v y; ;;
    "sql") chkOpt d v y; ;;
    ".v")  putMsg $NOR_PUTVAR $version; ;;
    ".u")  putMsg $NOR_PUTVAR "$username  $password"; ;;
    ".d")  putMsg $NOR_PUTVAR $database; ;;
    "ver") ;;
    "chp") chkOpt v;
           mysqladmin -u$username -p$password password $v;
           if [[ $? -eq 0 ]];then sed -i "s/$password/$v/g" $0; fi;
           exit; ;;
       *)  putMsg $ERR_ACTIVL $a; ;;
esac

setSql; 

if [[ -n $d ]];then
    putMsg $NOR_HITDBN "$d";
fi
if [[ -n $t ]];then
    putMsg $NOR_HITTBN "$t";
fi
if [[ -n $sql ]];then
    putMsg $NOR_PUTSQL "$sql";
fi


#confirm
if [[ $noConfirm -eq 1 ]];then exit; fi;

#format
if [[ $g == "1" ]];then sql="$sql\\G"; fi

    
#output
if [[ $a == "sd" ]];then
    res=$(echo "$sql" | mysql -u"$username" -p"$password" -A | tee $dbCacheFile | nl);
elif [[ $a == "st" ]];then
    res=$(echo "$sql" | mysql -u"$username" -p"$password" -A | tee $tbCacheFile | nl);
else
    res=$(echo "$sql" | mysql -u"$username" -p"$password" -A);
fi
res="${res//\`/}"


echo -e $fvio
if [[ $f ]];then
    if [[ $f == "c" ]];then
        putMsg $NOR_PUTRES "$res" | column -t
    elif [[ ${f:0:1} == "c" ]];then
        putMsg $NOR_PUTRES "$res" | cut -f ${f:1} | column -t
    else
        putMsg $NOR_PUTRES "$res" | cut -f $f
    fi
else
    putMsg $NOR_PUTRES "$res"
fi
echo -e $ccls
