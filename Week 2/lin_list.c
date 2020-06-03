/*
Title: Linear List
ShortSum: Linear List storing strings readed from file
Descr: 
    Assignment Week 2
    Read strings from file, output in reverse order + output in original order
Author: Robin Steidle
LastEdit: 26.05.2020
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
            printf("Couldn't find the file!\n");
            exit(EXIT_FAILURE);
        }
    }


    // Read File
    char chunk[256];
    while(fgets(chunk, sizeof(chunk), fp)) {
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

    LinListFree(ptr_first);

    fclose(fp);
}

// Create new cell and return pointer to it
LinList_p LinListAllocCell(char *payload) {
    LinList_p cell = (LinList_p) malloc(sizeof(LinListCell));
    cell->payload = strdup(payload);
    cell->next = NULL;
    return(cell);
}

// Free allocated memory of cell junk is pointing to
void LinListFreeCell(LinList_p junk) {
    free(junk->payload);
    free(junk);
}

// Free allocated memory of linear list
void LinListFree(LinList_p junk) {
    LinList_p ptr;
    while(ptr_first) {
        ptr = LinListExtractFirst(ptr_first);
        LinListFree(ptr);
    }
}

// inserts cell at the beginning of list; Returns pointer to the new cell
LinList_p LinListInsertFirst(LinList_p anchor, LinList_p newcell) {
    newcell->next = anchor;
    return(newcell);
}

// Removes cell from list and returns pointer to removed cell
LinList_p LinListExtractFirst(LinList_p anchor) {
    if(anchor==NULL) {
        return(NULL);
    }
    LinList_p ptr = anchor;
    ptr_first = ptr->next;
    return(ptr);
}

// prints every cell-payload in list
void Listprint(LinList_p fptr) {
    while(fptr) {
        printf("%s\n", fptr->payload);
        fptr = fptr->next;
    }
}

// reverse list, prints it and free memory of the new list
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
