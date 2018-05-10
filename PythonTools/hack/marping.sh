#!/bin/bash

if [ $# -ne 1 ]; then
	echo "使用方法：./arping.sh 网段地址"
	exit 1
fi

ip1=$(echo $1 | cut -d"." -f1)
ip2=$(echo $1 | cut -d"." -f2)
ip3=$(echo $1 | cut -d"." -f3)
prefix=$ip1.$ip2.$ip3

for ip4 in $(seq 254); do
	arping -c 1 $prefix.$ip4 &> /dev/null && echo $prefix.$ip
done
