/*
Title: Random Sequence Generator
ShortSum: Generates a sequence of random numbers between 0 (included) and MAXNUM (excluded)
Author: Robin Steidle
Version: 0.2
LastEdit: 12.05.2020
*/

#define MAXNUM 1000

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main() {
    // for more randomness: use time as seed
    srand(time(0));

    int n=10; // Length of sequence

    for (int i=0; i<=n; i++) {
        int num = rand()%MAXNUM;
        printf("%d\n", num);
    }
}