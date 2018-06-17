#!/bin/bash
#[09/May/2018:07:59:32]

UsrAgent=$1


cat /var/log/httpd/access_log | awk '
BEGIN{
    dan="\033[31m"
    suc="\033[32m"
    pri="\033[34m"
    war="\033[33m"
    vio="\033[35m"
    inf="\033[36m"
    def="\033[37m"
    cls="\033[0m"
    usrAgent=$useragent
}
{
    if("'"$UsrAgent"'") print vio "user-agent: " $12$13$14$15$16$17$18$19$20$21$22$23$24$25$26$27$28$29$30$31$32 cls

    
    len=length($10);
    len=3-len;
    while((len--)>0)
        $10=$10" "

    len=length($6);
    len=6-len;
    while((len--)>0)
        $6=$6" "

    print war $1"\t" cls, 
    suc substr($4,5,3)"/"substr($4,2,2)" "substr($4,14,8) cls,
    substr($6,2,5),
    $9,
    $10,
    inf $7 cls
}'
