#include <stdio.h>

class B{
public:
  virtual int prva()=0;
  virtual int druga(int)=0;
};

class D: public B{
public:
  virtual int prva(){return 42;}
  virtual int druga(int x){return prva()+x;}
};

typedef int (*pfun1)();
typedef int (*pfun2)(B*, int);

void funkcija(B* pb){
    int** vtable = *(int***) pb;
    //printf("prva()=%d\n", pb->prva());
    printf("prva()=%d\n", ((pfun1)vtable[0])());
    
    //printf("druga(10)=%d\n", pb->druga(10));
    printf("druga(10)=%d\n", ((pfun2)vtable[1])(pb, 10));
}

int main(){
    D* pd = new D;
    funkcija((B*) pd);

    return 0;
}