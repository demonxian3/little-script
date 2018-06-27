#!/bin/bash

#grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' /var/log/secure|sort|uniq -c > illegal_IP.tmp
#lastb |awk '{print $3}'|sort|uniq -c

#2018-01-19 发现BUG 如果出现一行IP是空的如下，会导致奇偶顺序破坏
#    4 12.145.151.21
#    3 112.113.50.38
#    3
#    5 117.34.51.66 
#空行产生的原因是ssh没有输入用户名导致 secure 文件里的 Invalid行中 awk print 10列不是IP地址而是空的
#解决办法 过滤Received 

scanIP=`grep -e 404 /var/log/httpd/access_log | awk '{print $1}'|sort |uniq -c`
#scanIP=`lastb | awk '{print $3}'|sort|uniq -c`

n=0
needban=0
for i in $scanIP
do
  if (( $n%2 == 0 )); then             #COUNT
     if [ $i -ge 10 ] ;then
	echo yes
        needban=1
        count=$i
     fi
  else
     if [ $needban -eq 1 ]; then       #ADDRESS
        IP=$i
        banIP=$IP			#删除最后一个字符:
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

