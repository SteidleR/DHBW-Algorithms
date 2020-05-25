/*
Title: Linear List
ShortSum: Linear List storing strings
Descr: 
    Assignment Week 2
    Read amount of string, output in reverse order + output in original order
Author: Robin Steidle
LastEdit: 25.05.2020
*/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct lin_list
{
    char *payload;
    struct lin_list *next;
}LinListCell, *LinList_p;


LinList_p LinListAllocCell(char*);
void LinListFreeCell(LinList_p);
void LinListFree(LinList_p);
LinList_p LinListInsertFirst(LinList_p, LinList_p);
LinList_p LinListExtractFirst(LinList_p);
void Listprint(LinList_p);
void RevList(LinList_p);

LinList_p ptr_first = NULL;

void main(int argc, char *argv[]) {
    FILE *fp;
    if(argc > 2) {
        printf("[ERROR] Too much arguments\n");
        exit(EXIT_FAILURE);
    }
    if(argc == 1) {
        printf("[ERROR] Need 1 argument!\n");
        exit(EXIT_FAILURE);
    }
    if (argc == 2) {
        fp = fopen(argv[1], "r");
        if(!fp) {
            printf("Couldn't find the file or the file is empty!");
            exit(EXIT_FAILURE);
        }
    }

    char chunk[256];
    while(fgets(chunk, sizeof(chunk), fp) != NULL) {
        int len = strlen(chunk);
        chunk[len-1] = *"";
        printf("%s\n",chunk);
        LinList_p cell = LinListAllocCell(chunk);
        ptr_first = LinListInsertFirst(ptr_first, cell);
    }

    printf("----  Reverse Order  ----\n");
    Listprint(ptr_first);

    printf("---- Original Order ----\n");
    RevList(ptr_first);
}


LinList_p LinListAllocCell(char *payload) {
    LinList_p cell = malloc(sizeof(LinListCell));
    cell->payload = strdup(payload);
    cell->next = NULL;
    return(cell);
}


void LinListFreeCell(LinList_p junk) {
    free(junk->payload);
    free(junk);
}


void LinListFree(LinList_p junk) {
    LinList_p ptr = junk;
    while(ptr->next) {
        junk = ptr;
        ptr = ptr->next;
    }
}


LinList_p LinListInsertFirst(LinList_p anchor, LinList_p newcell) {
    newcell->next = anchor;
    return(newcell);
}


LinList_p LinListExtractFirst(LinList_p anchor) {
    if(anchor==NULL) {
        return(NULL);
    }
    LinList_p ptr = anchor;
    ptr_first = ptr->next;
    return(ptr);
}


void Listprint(LinList_p fptr) {
    while(fptr) {
        printf("%s\n", fptr->payload);
        fptr = fptr->next;
    }
}


void RevList(LinList_p fptr) {
    LinList_p ptr_first_rev = NULL, ptr;

    while(fptr) {
        ptr = LinListAllocCell(fptr->payload);
        ptr_first_rev = LinListInsertFirst(ptr_first_rev, ptr);
        fptr = fptr->next;
    }

    Listprint(ptr_first_rev);
    LinListFree(ptr_first_rev);
}