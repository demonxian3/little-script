#!/bin/bash

ifconfig | awk '
NR==1{d1=substr($1,1,4)}
NR==11{d2=substr($1,1,2)}
NR==20{d3=substr($1,1,5)}
NR==2||NR==4||NR==12||NR==21{
  if(NR==2)print d1"\t"$2;
  if(NR==4)print $1"\t"$2;
  if(NR==12)print d2"\t"$2;
  if(NR==21)print d3"\t"$2;
}
'

