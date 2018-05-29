#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int getDigit(char ch){
    if ( ch >= '0' && ch <= '9')
        return ch - '0';
    if( ch >= 'A' && ch <= 'F' )
        return ch - 'A' + 10;
    if(ch >= 'a' && ch <= 'f')
        return ch - 'a' + 10;

    return -1;
}

char * hex2ascii(char * s){

    int i, j, t, digit, len;
    char * str = malloc(sizeof(char) * 255);

    i = j = t = 0;
    len = strlen(s);

    while( *(s+i) != 0 ){
        int digit = getDigit(*(s+i));
        if(!t){
            str[j] = digit * 16;
            t = 1;
        }else{
            str[j++] += digit;
            t = 0;
        }
        i++;
    }

    str[j] = '\0';
    return str;
}

void main(){
    char *hex = "68656c6c6f2064656d6f6e\0";
    char *res = hex2ascii(hex);
    printf("%s\n", res); 			//hello demon
}
