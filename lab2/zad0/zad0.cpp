#include <iostream>
#include <assert.h>
#include <stdlib.h>

struct Point
{
    int x;
    int y;
};
struct Shape
{
    enum EType
    {
        circle,
        square,
        rhomb
    };
    EType type_;
};
struct Circle
{
    Shape::EType type_;
    double radius_;
    Point center_;
};
struct Square
{
    Shape::EType type_;
    double side_;
    Point center_;
};
struct Rhomb{
    Shape::EType type_;
    double side_;
    Point center_;
};
void drawSquare(struct Square *)
{
    std::cerr << "in drawSquare\n";
}
void drawCircle(struct Circle *)
{
    std::cerr << "in drawCircle\n";
}
void drawRhomb(struct Rhomb *){
    std::cerr << "in drawRhomb\n";
}
void drawShapes(Shape **shapes, int n)
{
    for (int i = 0; i < n; ++i)
    {
        struct Shape *s = shapes[i];
        switch (s->type_)
        {
        case Shape::square:
            drawSquare((struct Square *)s);
            break;
        case Shape::circle:
            drawCircle((struct Circle *)s);
            break;
        case Shape::rhomb:
            drawRhomb((struct Rhomb *)s);
            break;
        default:
            assert(0);
            exit(0);
        }
    }
}
/**
 * Dodajte metodu moveShapes koja pomiče oblike zadane prvim argumentom za 
 * translacijski pomak određen ostalim argumentima. Ispitajte dodanu funkcionalnost.
 **/ 
void moveShapes(Shape **shapes, int n, Point* moves){
    for (int i = 0; i < n; ++i){
        struct Shape *s = shapes[i];
        switch (s->type_)
        {
        case Shape::square:
            ((struct Square*)s)->center_.x += moves[i].x;
            ((struct Square*)s)->center_.y += moves[i].y;
            break;
        case Shape::circle:
            ((struct Circle*)s)->center_.x += moves[i].x;
            ((struct Circle*)s)->center_.y += moves[i].y;
            break;
        case Shape::rhomb:
            ((struct Square*)s)->center_.x += moves[i].x;
            ((struct Square*)s)->center_.y += moves[i].y;
            break;
        default:
            assert(0);
            exit(0);
        }
    }
}
void print_center(Shape **shapes, int n){
    for(int i = 0; i < n; i++){
        struct Shape *s = shapes[i];
        switch (s->type_)
        {
        case Shape::square:
            printf("Square center x: %d, y:%d\n", ((struct Square*)s)->center_.x, ((struct Square*)s)->center_.y);
            break;
        case Shape::circle:
            printf("Square center x: %d, y:%d\n", ((struct Circle*)s)->center_.x, ((struct Circle*)s)->center_.y);
            break;
        case Shape::rhomb:
            printf("Rhomb center x: %d, y:%d\n", ((struct Rhomb*)s)->center_.x, ((struct Rhomb*)s)->center_.y);
            break;
        default:
            assert(0);
            exit(0);
        }
    }
}
int main()
{
    Shape *shapes[5];
    shapes[0] = (Shape *)new Circle;
    shapes[0]->type_ = Shape::circle;
    shapes[1] = (Shape *)new Square;
    shapes[1]->type_ = Shape::square;
    shapes[2] = (Shape *)new Square;
    shapes[2]->type_ = Shape::square;
    shapes[3] = (Shape *)new Circle;
    shapes[3]->type_ = Shape::circle;
    //dodani romb
    shapes[4] = (Shape *)new Rhomb;
    shapes[4]->type_ = Shape::rhomb;
    
    printf("%ld", sizeof(shapes) / sizeof(shapes[0]));
    drawShapes(shapes, sizeof(shapes) / sizeof(shapes[0]));

    //Prije translacije
    print_center(shapes, sizeof(shapes) / sizeof(shapes[0])); //Aborted (core dumped) ukoliko ne dodamo case za rhomb

    //Isprobajte dodanu funkcionalnost
    struct Point points[sizeof(shapes) / sizeof(shapes[0])] = {
        {.x = 1, .y = 2},
        {.x = 3, .y = 4},
        {.x = 5, .y = 6}, 
        {.x = 7, .y = 8},
        {.x = 9, .y = 10} //za rhomb
    };
    moveShapes(shapes, sizeof(shapes) / sizeof(shapes[0]), points);
    //Nakon translacije
    print_center(shapes, sizeof(shapes) / sizeof(shapes[0]));
}
