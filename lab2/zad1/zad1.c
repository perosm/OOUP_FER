#include <stdio.h>
#include <string.h>

//criterion functions
int gt_char(const void *a, const void *b){
    return ((int)*(char*) a > (int)*(char*)b) ? 1 : 0; //return 1 if the first argument is > the second
}

int gt_int(const void *a, const void *b){
    return (*(int*) a > *(int*)b) ? 1 : 0; //return 1 if the first argument is > the second
}

int gt_str(const void *a, const void *b){
    return strcmp(*(const char**) a, *(const char**)b) >= 1 ? 1 : 0; //*(char const**)const void* -> char const*
}

const void* mymax(const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *)){
    /**
     * base - pointer to the first element of the array to be sorted
     * nmemb - number of elements in the array pointed by base
     * size - size in bytes of each element in the array
     * compar - function that compares two elements
    */
    const void* max = base;
    for(int i = 1; i < nmemb; i++){
        const void* a = base + i * size;
        //printf("a=%d - b=%d ----> veći? %d\n", *(int *)a, *(int *)max, compar(a, max));
        //printf("a=%c - b=%c ----> veći? %d\n", *(char *)a, *(char *)max, compar(a, max));
        //printf("a=%s - b=%s ----> veći? %d\n", *(const char**)a, *(const char **)max, compar(a, max));
        max = (compar(a, max) == 1) ? a : max;
    }

    return max;
}


int main(){
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    const void* max_int = mymax(&arr_int, sizeof(arr_int) / sizeof(arr_int[0]), sizeof(arr_int[0]), gt_int);
    printf("Najveći int: %d\n", *(int*) max_int);
    char arr_char[]="Suncana strana ulice";
    const void* max_char = mymax(&arr_char, sizeof(arr_char) / sizeof(arr_char[0]), sizeof(arr_char[0]), gt_char);
    printf("Najveći char: %c\n", *(char*)max_char);
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",  
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };
    const void* max_str = mymax(&arr_str, sizeof(arr_str) / sizeof(arr_str[0]), sizeof(arr_str[0]), gt_str);
    printf("Najveći string: %s\n", *(const char**)max_str);

    return 0;
}