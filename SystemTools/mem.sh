#!/bin/bash

#while [ 1 ] 
#do
#clear
free -m | grep Mem: | awk '{per=$3*100/$2;print "\033[31mCurrent Mem\033[36m:"substr(per,1,5)"%\033[0m"}'
#sleep 1
#done
