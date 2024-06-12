#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


//**************************************Unary function**************************************
struct Unary_Function;

typedef struct{
    double (*value_at)(struct Unary_Function* this, double x);
    double (*negative_value_at)(struct Unary_Function* this, double x);
} VTableUnary_Function;

struct Unary_Function{
    //private
    int lower_bound;
    int upper_bound;
    //public
    void (*tabulate)(struct Unary_Function* this);
    bool (*same_function_for_ints)(struct Unary_Function* f1, struct Unary_Function* f2, double tolerance);
    VTableUnary_Function* vtable;
};

double negative_value_at(struct Unary_Function* this, double x){
    return this->vtable->value_at(this, x);
}

void tabulate(struct Unary_Function* this){
    for(int x = this->lower_bound; x <= this->upper_bound; x++){
        printf("f(%d)=%lf\n", x, this->vtable->value_at(this, x));
    }
}

static bool same_function_for_ints(struct Unary_Function* f1, struct Unary_Function* f2, double tolerance){
    if(f1->lower_bound != f2->lower_bound) return false;
    if(f1->upper_bound != f2->upper_bound) return false;
    for(int x = f1->lower_bound; x <= f1->upper_bound; x++){
        double delta = f1->vtable->value_at(f1, x) - f2->vtable->value_at(f1, x);
        if(delta < 0) delta = -delta;
        if(delta > tolerance) return false;
    }
    return true;
}


const struct Unary_FunctionFactory{
   struct Unary_Function*(*new)(int lb, int ub);
} Unary_Function;

struct Unary_Function* new_Unary(int lb, int ub){
    struct Unary_Function* unary_function = (struct Unary_Function*)malloc(sizeof(struct Unary_Function));
    unary_function->lower_bound = lb;
    unary_function->upper_bound = ub;
    unary_function->same_function_for_ints = &same_function_for_ints;
    unary_function->tabulate = &tabulate;
    unary_function->vtable = (VTableUnary_Function*)malloc(sizeof(VTableUnary_Function));
    unary_function->vtable->negative_value_at = &negative_value_at;

    return unary_function;
}

const struct Unary_FunctionFactory Unary_Function = {.new=&new_Unary};


//**************************************Linear**************************************

struct Linear;

typedef struct{
    double (*value_at)(struct Unary_Function* this, double x);
    double (*negative_value_at)(struct Unary_Function* this, double x);
} LinearVTable;

struct Linear{
    LinearVTable* vtable;
    double a;
    double b;
};

double linear_value_at(struct Unary_Function* this, double x){
    struct Linear* linear = (struct Linear*) this;
    printf("a=%f, b=%f", linear->a, linear->b);
    return linear->a*x + linear->b;
}

const struct LinearFactory{
    struct Unary_Function* (*new)(int lb, int ub, double a_coef, double b_coef);
} Linear;

struct Unary_Function* new_Linear(int lb, int ub, double a_coef, double b_coef){
    struct Unary_Function* unary_function = Unary_Function.new(lb, ub);
    struct Linear* linear = (struct Linear*) malloc(sizeof(struct Linear));
    linear->a = a_coef;
    linear->b = b_coef;
    linear->vtable = (LinearVTable*)malloc(sizeof(LinearVTable));
    linear->vtable->value_at = &linear_value_at;
    linear->vtable->negative_value_at = &negative_value_at;
    unary_function->vtable = (VTableUnary_Function*)linear->vtable;
    
    return unary_function;
}

const struct LinearFactory Linear = {.new=&new_Linear};


//**************************************Square**************************************

struct Square;

typedef struct{
    double (*value_at)(struct Unary_Function* this, double x);
    double (*negative_value_at)(struct Unary_Function* this, double x);
} VTableSquare;

struct Square{
    VTableSquare* vtable;
};

double square_value_at(struct Unary_Function* this, double x){
    struct Square* square = (struct Square*) this; 
    return x*x;
}


const struct SquareFactory{
    struct Unary_Function* (*new)(int lb, int ub);
} Square;

struct Unary_Function* new_Square(int lb, int ub){
    struct Unary_Function* unary_function = Unary_Function.new(lb, ub);
    struct Square* square = (struct Square*) malloc(sizeof(struct Square));
    square->vtable = (VTableSquare*)malloc(sizeof(VTableSquare));
    square->vtable->value_at = &square_value_at;
    square->vtable->negative_value_at = &negative_value_at;
    unary_function->vtable = (VTableUnary_Function*)square->vtable;

    return unary_function;
}

const struct SquareFactory Square = {.new=&new_Square};


int main(){
    struct Unary_Function *f1 = Square.new(-2, 2); // new Square(-2, 2);
    f1->tabulate(f1);
    struct Unary_Function *f2 = Linear.new(-2, 2, 5, 2);
    f2->tabulate(f2);
    printf("f1==f2: %s\n", same_function_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vtable->negative_value_at(f2, 1.0));
    
    free(f1);
    free(f2);
    return 0;
}