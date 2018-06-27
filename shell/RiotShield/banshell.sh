#!/bin/bash

#clear iptables when time is 00:00
#now=$(date +%H:%M:%S)
#if [[ $now == "16:03:30" ]];then
#    `iptables -F`
#fi

# [Notice] clear iptables
`iptables -F`

#calculate the time for ban time
curHour=`date +%H`
curMinu=`date +%M`

starttime="$curHour:$curMinu"

curMinu=$(($curMinu + 30))
if [[ $curMinu -gt 59 ]]; then
    curHour=$(($curHour + 1))
    curMinu=$(($curMinu % 60))
fi

stoptime="$curHour:$curMinu"

dangerIP=`cat /var/log/httpd/access_log | grep 404 | awk '{print $1}' | sort  | uniq -c | awk '{if($1>30)print $2}'`

for i in $dangerIP; do
    res=`iptables -nvL | grep $i`
    if [[ $res == "" ]]; then
        echo $(date) $i >> /var/log/mybanip.log
        `iptables -A INPUT -s $i -m time --timestart $starttime --timestop $stoptime -j DROP `
    else
        echo "go"
    fi
done

