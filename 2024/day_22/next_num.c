#include <stdlib.h>

int mod = (1<<24)-1;
int *next_number(int num, int times) {
    int *res = malloc(times*sizeof(int));
    for (int i = 0; i < times; i++) {
        num = (num ^ (num<<6)) & mod;
        num = (num ^ (num>>5)) & mod;
        num = (num ^ (num<<11)) & mod;
        res[i] = num;
    }
    return res;
}

void free_memory(int *arr) {
    free(arr);
}