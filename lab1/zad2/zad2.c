#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


//**************************************Unary function**************************************
struct Unary_Function;

typedef double (*PTRFUN)(struct Unary_Function*, double);

struct Unary_Function{
    PTRFUN* vptr;
    //private
    int lower_bound;
    int upper_bound;
    //public
    // void (*tabulate)(struct Unary_Function* this);
} Unary_Function;

double negative_value_at(struct Unary_Function* this, double x){
    return -(*(PTRFUN)(this->vptr[0]))(this, x);
}

PTRFUN vtable_unary_function[2] = {NULL, &negative_value_at};

void tabulate(struct Unary_Function* this){
    for(int x = this->lower_bound; x <= this->upper_bound; x++){
        printf("f(%d)=%lf\n", x, (*(PTRFUN)(this->vptr[0]))(this, x));
    }
}

static bool same_function_for_ints(struct Unary_Function* f1, struct Unary_Function* f2, double tolerance){
    if(f1->lower_bound != f2->lower_bound) return false;
    if(f1->upper_bound != f2->upper_bound) return false;
    for(int x = f1->lower_bound; x <= f1->upper_bound; x++){
        double delta = (*(PTRFUN)(f1->vptr[0]))(f1, x) - (*(PTRFUN)(f2->vptr[0]))(f2, x);
        if(delta < 0) delta = -delta;
        if(delta > tolerance) return false;
    }
    return true;
}

void new_Unary(struct Unary_Function* this, int lb, int ub){
    this->lower_bound = lb;
    this->upper_bound = ub;
    // this->tabulate = &tabulate;
    this->vptr = vtable_unary_function;
}


//**************************************Linear**************************************

struct LinearVTable{
    double (*value_at)(struct Unary_Function* this, double x);
    double (*negative_value_at)(struct Unary_Function* this, double x);
};

struct Linear{
    PTRFUN* vptr;
    int lower_bound; //dolaze prije a i b
    int upper_bound;
    double a;
    double b;
} Linear;

double linear_value_at(struct Unary_Function* this, double x){
    struct Linear* linear = (struct Linear*) this;
    //printf("a=%f, b=%f\t", linear->a, linear->b);
    return linear->a*x + linear->b;
}

PTRFUN vtable_linear[2] = {&linear_value_at, &negative_value_at};

const struct LinearFactory{
    struct Unary_Function* (*new)(int lb, int ub, double a_coef, double b_coef);
} LinearClass;

struct Unary_Function* new_Linear(int lb, int ub, double a_coef, double b_coef){
    struct Linear* linear = (struct Linear*) malloc(sizeof(Linear));
    new_Unary((struct Unary_Function*) linear, lb, ub);
    linear->vptr = vtable_linear;
    linear->a = a_coef;
    linear->b = b_coef;

    return (struct Unary_Function*) linear;
}

const struct LinearFactory LinearClass = {.new=&new_Linear};


//**************************************Square**************************************

struct Square{
    PTRFUN* vptr;
} Square;

double square_value_at(struct Unary_Function* this, double x){
    return x*x;
}

PTRFUN vtable_square[2] = {&square_value_at, &negative_value_at};

const struct SquareFactory{
    struct Unary_Function* (*new)(int lb, int ub);
} SquareClass;

struct Unary_Function* new_Square(int lb, int ub){
    struct Square* square = (struct Square*) malloc(sizeof(Square));
    new_Unary((struct Unary_Function*) square, lb, ub);
    square->vptr = vtable_square;
    return (struct Unary_Function*) square;
}

const struct SquareFactory SquareClass = {.new=&new_Square};


int main(){
    struct Unary_Function *f1 = SquareClass.new(-2, 2); // new Square(-2, 2);
    tabulate(f1); // f1->tabulate(f1);
    printf("sizeof(f1)=%ld\n", sizeof(f1));
    struct Unary_Function *f2 = LinearClass.new(-2, 2, 5, 2);
    printf("sizeof(f2)=%ld\n", sizeof(f2));
    tabulate(f2); // f1->tabulate(f2);
    printf("f1==f2: %s\n", same_function_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vptr[1](f2, 1.0));
    free(f1);
    free(f2);

    return 0;
}