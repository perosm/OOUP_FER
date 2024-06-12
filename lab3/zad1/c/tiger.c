#include <stdlib.h>

typedef char const* (*PTRFUN)();

//i) definirati konkretni tip ljubimca strukturom koja će osim 
//pokazivača na virtualnu tablicu imati i pokazivač na ime.
struct Tiger{
    PTRFUN* vtable;
    const char* name;
} Tiger;

//ii) implementirati funkcije ("metode"): name, greet i menu
char const* name(struct Tiger* this){
    return this->name;    
}

char const* greet(){
    return "Mijau!";
}

char const* menu(){
    return "mlako mlijeko.";
}

//iii) definirati virtualnu tablicu
PTRFUN tiger_vtable[3] = {name, greet, menu};

//iv) definirati funkciju za stvaranje novih objekata na gomili
//s prototipom void* create(char const* name)
void* create(char const* name){
    struct Tiger* tiger = (struct Tiger*) malloc(sizeof(struct Tiger));
    tiger->vtable = tiger_vtable;
    tiger->name = name;

    return tiger;
}

void* create_stack(char const* name){
    Tiger.name = name;
    Tiger.vtable = tiger_vtable;

    return &Tiger;
}