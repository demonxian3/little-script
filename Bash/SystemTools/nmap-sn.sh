grep -v "down"       | 
awk 'NR>5{print $0}' | 
awk '{
  if((NR-1)%3==0){
    printf $5
  }else if(NR%3==0){
     if($3 == "files"){
       print "\tThis is you\n"
     }
     else if(NR>4){
       print "\t"$3"\t"$4,$5,$6,$7,$8
     }
     else{ 
       print "\t"$3"\t"$4
     }
  }
}'

