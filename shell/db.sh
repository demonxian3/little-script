#!/bin/bash
#name:    qucik sql execution in shell
#version: 1.4
#author:  Khazix Li
#date:    2019/05/05
#help:    please change $username, $password, $database on line:8,9,10

#config
username=<your username>
password=<your password>
database=<your default database>

function help(){
cat <<EOF
usage: db <action> [<key> <value>]*
action:
    [record]
        sr => select \$c from \$d.\$t [where \$if]
        ir => insert into \$d.\$t(\$c) values(\$v)
        ur => update \$d.\$t set (\$v) [where \$if]
        dr => delete from \$d.\$t [where \$if]

    [tables]
        st  => show tables
        dt  => drop table \$d.\$t
        ct  => create table \$d.\$t(\$c)
        sct => show create table \$d.\$t
        dst => desc \$d.\$t

    [database]
        sd => show databases
        cd => create database \$d
        dd => drop database \$d

    [columns]
        cc => select ... from infor~.columns where table_name = \$d.\$t

    [variable]
        sv => show variables like '%\$v%'
        version => select version();

    [function]
        sql    => execute \$v;
        login  => enter interact shell
        backup => mysqldump \$d
        source => source \$v
        passwd => mysqladmin \$v
EOF
exit;
}

if [[ ! -n $1 ]];then
    help
fi

action=$1
shift

while [[ -n "$1" && -n "$2" ]];do
    case $1 in
        "d")   d=$2   ;;
        "t")   t=$2   ;;
        "c")   c=$2   ;;
        "v")   v=$2   ;;
        "f")   f=$2   ;;
        "if")  if=$2  ;;
        *) echo [WARNING]  $1 is invalid key ;;
    esac
    shift 2;
done

sql=""
needConfirm="0"
function checkDatabase(){
    if [[ -z $d ]];then
        echo '[key:d] database cannot empty';
        exit;
    fi
}

function checkTable(){
    if [[ -z $t ]];then
        echo '[key:t] table cannot empty';
        exit;
    fi
}

function checkColumn(){
    if [[ -z $c ]];then
        echo '[key:c] column cannot empty';
        exit;
    fi
}

function checkWhere(){
    if [[ -z $if ]];then
        echo '[key:if] condition cannot empty, if you want to delete data, please add "if all"';
        exit;
    fi;
}
function checkValue(){
    if [[ -z $v ]];then
        echo '[key:v] value cannot empty';
        exit;
    fi
}

function defaultField(){
    if [[ -z $c ]];then
        c="*";
    fi
}

function defaultDatabase(){
    if [[ -z $d ]];then
        d="$database";
    fi
}

case $action in
    "sr")
        checkTable; defaultField;

        if test -z $if ; then
            sql="select $c from $d.$t"
        else
            sql="select $c from $d.$t where $if"
        fi
        ;;
    "ir")
        needConfirm=1
        checkTable; checkValue;

        if test -z $c ; then
            sql="insert into $d.$t values($v);"
        else
            sql="insert into $d.$t($c) values($v);"
        fi
        ;;
    "ur")
        needConfirm=1
        checkTable; checkValue;

        if test -z $if ; then
            sql="update $d.$t set $v;"
        else
            sql="update $d.$t set $v where $if";
        fi
        ;;
    "dr")
        needConfirm=1
        checkTable; checkWhere;

        if [ $if == "all" ];then
            sql="delete from $d.$t;";
        else
            sql="delete from $d.$t where $if;";
        fi
    ;;
    "dt")
        checkTable;
        needConfirm=1
        sql="drop table $d.$t;";
    ;;
    "ct")
        checkTable;
        checkColumn;
        needConfirm=1
        sql="create table $d.$t ($c)";
    ;;
    "st")
        sql="show tables;";
    ;;
    "dst")
        checkTable;
        sql="desc $t";
    ;;
    "sct")
        checkTable;
        sql="show create table $d.$t";
    ;;
    "sd")
        sql="show databases;";
        execDirect=1;
    ;;
    "cd")
        checkDatabase;
        execDirect=1;
        sql="create database $d;";
    ;;
    "dd")
        checkDatabase;
        needConfirm=1;
        execDirect=1
        sql="drop database $d;";
    ;;
    "cc")
        checkTable;
        sql="select distinct 
            ORDINAL_POSITION, COLUMN_NAME,
            IS_NULLABLE, COLUMN_TYPE,
            COLUMN_DEFAULT, EXTRA,
            COLUMN_KEY, COLUMN_COMMENT 
            from information_schema.columns 
            where table_name = '$t'";
    ;;
    "sv")
        if [[ -z $v ]];then
            sql="show variables;"
        else
            sql="show variables like '%$v%'";
        fi
    ;;
    "login")
        mysql -u$username -p$password -A
        exit;
    ;;
    "backup")
        checkDatabase;
        mysqldump -u$username -p$password $d > $d.sql
        exit;
    ;;
    "passwd")
        checkValue;
        sed -i "s/$password/$v/g" $0
        mysqladmin -u$username -p$password password $v
        exit;
    ;;
    "source")
        checkDatabase;
        checkValue;
        needConfirm=1;
        execDirect=1;
        sql="use $d;source $v;"
    ;;
    "sql")
        needConfirm=1
        checkValue;
        sql="$v";
    ;;
    *)
        help;
    ;;
esac


#display
echo  "$sql"

#confirm
if [[ $needConfirm -eq 1 ]];then
    if [[ $1 != "ok" ]];then
        echo "[confirm]? please input 'ok' at the end of the command";
        exit;
    fi
fi

#format
if [[ $1 == "g" ]];then
    sql="$sql\\G";
fi

#execute
if [[ $execDirect -eq 1 ]];then
    result=$(echo "$sql" | mysql -u"$username" -p"$password" -A)
else
    defaultDatabase;
    result=$(echo "use $d;$sql" | mysql -u"$username" -p"$password" -A)
fi

#output
result="${result//\`/}"
if [[ $f ]];then
    echo "$result" | cut -f $f | column -t;
else
    echo "$result" | column -t;
fi
