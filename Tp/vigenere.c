#include <stdio.h>
#include <stdlib.h>

char* encj(char* msg, char* cle, int len_cle, int len_msg){
    int i = 0; 
    char* tmp = malloc(len_msg * sizeof(char) + 1);
    while (i<len_msg)
    {
        tmp[i] -= 'a';
        tmp[i] = (tmp[i] + (cle[i%len_cle] - 'a'))%26;
        tmp[i] += 'a';
        i++;
    }
    tmp[i] = '\o';
    return tmp;
}

char* dec(char* msg, char* cle, int len_cle, int len_msg){
    int i = 0; 
    char* tmp = malloc(len_msg * sizeof(char) + 1);
    while (i<len_msg)
    {
        tmp[i] += 'a';
        tmp[i] = (tmp[i] - (cle[i%len_cle] + 'a'))%26;
        tmp[i] -= 'a';
        i++;
    }
    tmp[i] = '\o';
    return tmp;
}

int main(int argc, char **argv){
    
}