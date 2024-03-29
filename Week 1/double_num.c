/*
Title: Double Numbers
ShortSum: Double the Numbers in a file
LongDescr: Reads Integers from a file or the stdin Pipe and outputs the double. File is passed as Command Line Argument.
Author: Robin Steidle
Version: 0.3
LastEdit: 13.05.2020
*/

#include <stdio.h>
#include <stdlib.h>

void main(int argc, char *argv[]) {
    if (argc > 2) {
        // to many Arguments
        printf("[ERROR]Expected 1 Argument, got %d!\n", argc-1);
        exit(EXIT_FAILURE);
    } else if (argc == 1) {
        // No additional Argument: get Numbers from stdin
        FILE *instream = fopen("/dev/stdin","r");
        char chunk[256];
        while(fgets(chunk,sizeof(chunk), instream) != NULL) {
            int n = atoi(chunk);
            //printf("%s *2:",chunk);
            printf("%d\n",n*2);
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
            int n = atoi(chunk);
            //printf("%s *2:",chunk);
            printf("%d\n",n*2);
        }
    }
}
    