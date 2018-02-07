netstat -ntpl | awk "-F[\: /]+" '
BEGIN{
  print "Type\t IP\t\t PORT\t PID\t PName\t"
}
NR!=1 && NR!=2 {
  if($1=="tcp6"){
    print $1"\t\t\t "$4"\t "$7"\t "$8
  }else{
    print $1"\t " $4"\t " $5"\t " $9"\t " $10;
  }
}'

