#include <stdlib.h>

typedef char const* (*PTRFUN)();

//i) definirati konkretni tip ljubimca strukturom koja će osim 
//pokazivača na virtualnu tablicu imati i pokazivač na ime.
struct Parrot{
    PTRFUN* vtable;
    const char* name;
} Parrot;

//ii) implementirati funkcije ("metode"): name, greet i menu
char const* name(struct Parrot* this){
    return this->name;    
}

char const* greet(){
    return "Sto mu gromova!";
}

char const* menu(){
    return "brazilske orahe.";
}

//iii) definirati virtualnu tablicu
PTRFUN parrot_vtable[3] = {name, greet, menu};

//iv) definirati funkciju za stvaranje novih objekata na gomili
//s prototipom void* create(char const* name)
void* create(char const* name){
    struct Parrot* parrot = (struct Parrot*) malloc(sizeof(struct Parrot));
    parrot->vtable = parrot_vtable;
    parrot->name = name;

    return parrot;
}

void* create_stack(char const* name){
    // struct Parrot parrot; //stvaramo na stogu
    Parrot.name = name;
    Parrot.vtable = parrot_vtable;

    return &Parrot;
}