#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

struct Animal{
  char const* namePtr; //pointer na ime ljubimca
  PTRFUN* vptr; //pointer na tablicu funkcija
};

struct Cat{
  char const* name;
};

struct Dog{
  char const* name;
};

char const* dogGreet(void){
  return "vau!";
}
char const* dogMenu(void){
  return "kuhanu govedinu";
}
char const* catGreet(void){
  return "mijau!";
}
char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

PTRFUN VTableCat[2] = {&catGreet, &catMenu};
PTRFUN VTableDog[2] = {&dogGreet, &dogMenu};

void animalPrintGreeting(struct Animal* animal){
  printf("%s pozdravlja: %s\n", animal->namePtr, (*(PTRFUN)(animal->vptr[0]))());
}

void animalPrintMenu(struct Animal* animal){
  printf("%s voli: %s\n", animal->namePtr, (*(PTRFUN)(animal->vptr[1]))());
}

struct Animal* constructCat(struct Animal* animal, char const* name){
  animal->namePtr = name;
  animal->vptr = (PTRFUN*) &VTableCat;
  for(int i = 0; i < sizeof(VTableCat) / sizeof(VTableCat[0]); i++){
    animal->vptr[i] = VTableCat[i];
  }
  return animal;
}

struct Animal* createCat(char name[]){
  struct Animal* animal = (struct Animal*) malloc(sizeof(struct Animal));
  struct Cat cat; // = (struct Cat*)malloc(sizeof(struct Cat));
  cat.name = name;
  
  return constructCat(animal, cat.name);
}

struct Animal* constructDog(struct Animal* animal, char const* name){
  animal->namePtr = name;
  animal->vptr = (PTRFUN*) &VTableDog;
  for(int i = 0; i < sizeof(VTableDog) / sizeof(VTableDog[0]); i++){
    animal->vptr[i] = VTableDog[i];
  }

  return animal;
}

struct Animal* createDog(char name[]){
  struct Animal* animal = (struct Animal*) malloc(sizeof(struct Animal));
  struct Dog dog; // = (struct Dog*) malloc(sizeof(struct Dog));
  dog.name = name;
  
  return constructDog(animal, dog.name);
}


void testAnimals(void){
  struct Animal* p1=createDog("Hamlet");
  struct Animal* p2=createCat("Ofelija");
  struct Animal* p3=createDog("Polonije");
  
  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);

  free(p1); 
  free(p2); 
  free(p3);
}
struct Animal** createNDogs(int n){
  struct Animal** dogs = (struct Animal**) malloc(n * sizeof(struct Animal));
  for(int i = 0; i < n; i++){
    printf("int i=%d", i);
    dogs[i] = createDog("Dog");
  }
  return dogs;
}

void testNDogs(){
  int n = 5;
  struct Animal** dogs = createNDogs(n);
  for(int i = 0; i < n; i++){
    animalPrintGreeting(dogs[i]);
    animalPrintMenu(dogs[i]);
  }

  free(dogs);
}

int main(){

  testAnimals();
  testNDogs();


  /**
   * TO DO:
   *
   * Nakon rješavanja zadatka, uspostavite vezu s terminologijom 
   * iz objektno orijentiranih jezika. Koji elementi vašeg rješenja bi 
   * korespondirali s podatkovnim članovima objekta, metodama, 
   * virtualnim metodama, konstruktorima, te virtualnim tablicama? 
  */
  return 0;
}