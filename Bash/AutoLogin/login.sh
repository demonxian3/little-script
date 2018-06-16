#!/bin/bash
# @Author:Demon
awk '
{
  host = $1;
  port = $2;
  user = $3;
  pass = $4;
  if($5)system("expect /tmp/ssh.exp "host" "port" "user" "pass" "$5);
  else  system("expect /tmp/ssh.exp "host" "port" "user" "pass);
}' loginfile

