#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>

typedef void* (*PTRFUN)();

void* myfactory(char const* libname, char const* ctorarg, const char* dynamic){
    /**
     * libname - ime biblioteke
     * ctorarg - argument za fju create
     * 
     * otvara biblioteku zadanu argumentom libname
     * ucitava funkciju create iz zadane biblioteke
     * te poziva funkciju create sa argumentom ctorarg
     * te dobiveni pokazivac na funkciju vraca pozivatelju
     * pretpostavka: trazena biblioteka se nalazi u tekucem
     * kazalu, te dekoriramo ime biblioteke tekucim kazalom 
     * i standardnom ekstenzijom (.so) za UNIX.
     * dlopen -https://pubs.opengroup.org/onlinepubs/009695399/functions/dlopen.html
     * dlsym - https://pubs.opengroup.org/onlinepubs/009695399/functions/dlsym.html
     * return:
    */
    
    char const* thisFolder = "./";
    char const* fileExtension = ".so";
    char* path = (char*) malloc(strlen(thisFolder) + strlen(libname) + strlen(fileExtension));
    void* animal;
    void* handle;
    PTRFUN create;
    strcpy(path, thisFolder);
    strcat(path, libname);
    strcat(path, fileExtension);
    
    //otvaranje biblioteke zadane argumentom libname
    handle = dlopen(path, RTLD_LOCAL | RTLD_LAZY);
    //pronalazak adrese funkcije i podatkovnih objekata
    if(strcmp(dynamic, "1")){
        create = dlsym(handle, "create");
        //poziva funkciju create sa argumentom ctorarg 
        animal = create(ctorarg);
    }else{
        create = dlsym(handle, "create_stack");
        animal = create(ctorarg);
    }
    
    return animal;
}