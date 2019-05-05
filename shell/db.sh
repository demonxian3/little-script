#!/bin/bash

#config
username=<yourusername>
password=<yourpassword>
d=<yourDefaultDatabase>


help="
    usage: db <action> [<key> <value>]*\n
    \n
    action: \n
        ss => select \$c from \$d.\$t [where \$if]\n
        st => show tables\n
        sd => show databases\n
        dt => desc \$d.\$t\n
        ii => insert into \$d.\$t(\$c) values(\$v)\n
        uu => update \$d.\$t set (\$v) [where \$if]\n
        dd => delete from \$d.\$t [where \$if]\n
        cc => select column_info from information_schema.columns where table_name = \$d.\$t
"

if [[ ! -n $1 ]];then
    echo -e $help
fi

action=$1
shift

while [[ -n "$1" && -n "$2" ]];do
    case $1 in
        "d")   d=$2   ;;
        "t")   t=$2   ;;
        "c")   c=$2   ;;
        "v")   v=$2   ;;
        "if")  if=$2  ;;
        *) echo [WARNING]  $1 is invalid key ;;
            esac
    shift 2;
done

sql=""

case $action in
    "ss")
        if test -z $t ; then
            echo [key:t] cannot empyt
            exit;
        fi

        if test -z $c ; then
            c="*"
        fi

        if test -z $if ; then
            sql="select $c from $d.$t;"
        else
            sql="select $c from $d.$t where $if;"
        fi
        ;;
    "ii")
        if test -z $t ; then
            echo '[key:t] cannot empyt'
            exit;
        fi
        if test -z $v ; then
            echo '[key:v] cannot empyt'
        fi

        if test -z $c ; then
            sql="insert into $d.$t values($v);"
        else
            sql="insert into $d.$t($c) values($v);"
        fi
        ;;
    "uu")
        if test -z $t ; then
            echo '[key:t] cannot empyt'
            exit;
        fi
        if test -z $v ; then
            echo '[key:v] cannot empyt'
            exit;
        fi

        if test -z $if ; then
            sql="update $d.$t set $v;"
        else
            sql="update $d.$t set $v where $if";
        fi
        ;;
    "dd")
        if test -z $t ; then
            echo '[key:t] cannot empyt'
            exit;
        fi
        if test -z $if ; then
            echo '[key:if]=>[all] cannot empyt'
            exit;
        else
            if [ $if == "all" ];then
                sql="delete from $d.$t;";
            else
                sql="delete from $d.$t where $if;";
            fi
        fi
    ;;
    "sd")
        sql="show databases;";
    ;;
    "st")
        sql="use $d;show tables;";
    ;;
    "dt")
        if test -z $t ; then
            echo '[key:t] cannot empyt'
            exit;
        fi
        sql="desc $t;";
    ;;
    "cc")
        if test -z $t ; then
            echo '[key:t] cannot empyt'
            exit;
        fi
        sql="select distinct ORDINAL_POSITION,COLUMN_NAME,IS_NULLABLE,COLUMN_TYPE,COLUMN_DEFAULT,EXTRA,COLUMN_KEY,COLUMN_COMMENT from information_schema.columns where table_name = '$t'";

esac

echo  "$sql"

if [[ $1 == "g" ]];then
    sql="$sql\\G";
fi
echo "use $d;$sql" | mysql -u"$username" -p"$password"

