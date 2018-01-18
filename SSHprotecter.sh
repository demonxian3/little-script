#!/bin/bash
#@Auth: Demon
#@Date: 2018-01-18
#@Desc: ban the host which try to  burst the root's password for ssh

#grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' /var/log/secure|sort|uniq -c > illegal_IP.tmp
#lastb |awk '{print $3}'|sort|uniq -c

scanIP=`grep -e Invalid  /var/log/secure | awk '{print $10}'|sort |uniq -c`
n=0
needban=0
for i in $scanIP
do
  if (( $n%2 == 0 )); then             #COUNT
     if [ $i -gt 10 ] ;then
        needban=1
        count=$i
     fi
  else
     if [ $needban -eq 1 ]; then       #ADDRESS
        banIP=$i
        needban=0
 
        #BAN
        if [ -z "`/sbin/iptables -vnL INPUT | grep $banIP`" ]; then
            echo "[BAN] $banIP ($count) `date`" >> /var/log/ban.log         #LOG
           `/sbin/iptables -I INPUT -s $banIP -m state --state NEW,RELATED,ESTABLISHED -j DROP`
        fi
     fi
  fi
  n=`expr $n + 1 `
done

