/*
Title: Random Sequence Generator
ShortSum: Generates a sequence of random numbers between 0 (included) and MAXNUM (excluded)
Author: Robin Steidle
Version: 0.31
LastEdit: 12.05.2020
*/

#define MAXNUM 1000

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main(int argc, char *argv[]) {
    int l; // Length of sequence

    if (argc > 2) {
        printf("[ERROR]Expected 1 Argument, got %d!\n", argc-1);
        exit(EXIT_FAILURE);
    } else if (argc == 1) {
        printf("[WARNING]Expected 1 Argument, got 0. Default value is used!\n");
        l = 10;
    } else {
        l = atoi(argv[1]);
    }

    // for more randomness: use time as seed
    srand(time(0));

    for (int i=0; i<l; i++) {
        int num = rand()%MAXNUM;
        printf("%d\n", num);
    }
}