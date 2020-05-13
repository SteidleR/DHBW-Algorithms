/*
Title: Reverse String
ShortSum: Reverse the String readed from file or stdin PIPE
Author: Robin Steidle
Version: 0.3
LastEdit: 13.05.2020
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void reverse(char*);

void main(int argc, char *argv[]) {
    if (argc > 2) {
        // to many Arguments
        printf("[ERROR]Expected 1 Argument, got %d!\n", argc-1);
        exit(EXIT_FAILURE);
    } else if (argc == 1) {
        // Use stdin PIPE
        FILE *instream = fopen("/dev/stdin","r");
        char chunk[256];
        while(fgets(chunk,sizeof(chunk), instream) != NULL) {
            int len = strlen(chunk);
            chunk[len-1] = *"";
            //printf("%s: ",chunk);
            reverse(chunk);
            printf("%s\n",chunk);
        }
    } else {
        // 1 Argument -> file name
        FILE *fp = fopen(argv[1],"r");
        if (fp==NULL) {
                printf("[ERROR]Unable to open file!");
                exit(EXIT_FAILURE);
        }
        char chunk[256];
        while(fgets(chunk, sizeof(chunk), fp) != NULL) {
            int len = strlen(chunk);
            chunk[len-1] = *"";
            //printf("%s: ",chunk);
            reverse(chunk);
            printf("%s\n",chunk);
        }
    }
}

void reverse(char *Str) {
    char temp;
    int i=0, j=0;
    j = strlen(Str)-1;
    while (i<j) {
        temp = Str[i];
        Str[i] = Str[j];
        Str[j] = temp;
        i++;
        j--;
    }
}