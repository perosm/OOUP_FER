#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

class Point{
public:
    int x;
    int y;
};
class Shape
{
public:
    virtual void draw() = 0;
    virtual void move(Point* p) = 0;
};
class Circle : public Shape
{
private:
    Point center_;
    double radius_;
public:
    virtual void draw(){
        std::cerr << "in drawCircle\n";
    }
    virtual void move(Point* p){
        std::cout << "before: x=" << center_.x << ", y=" << center_.y << std::endl;
        center_.x += p->x;
        center_.y += p->y;
        std::cout << "after: x=" << center_.x << ", y=" << center_.y << std::endl;
    }
};
class Square : public Shape
{
private:
    Point center_;
    double side_;
public:
    virtual void draw(){
        std::cerr << "in drawSquare\n";
    }
    virtual void move(Point* p){
        std::cout << "before: x=" << center_.x << ", y=" << center_.y << std::endl;
        center_.x += p->x;
        center_.y += p->y;
        std::cout << "after: x=" << center_.x << ", y=" << center_.y << std::endl;
    }
};
class Rhomb : public Shape{
private:
    Point center_;
    double base_;
    double height_;
public:
    virtual void draw(){
        std::cerr << "in drawRhomb\n";
    }
    virtual void move(Point* p){
        std::cout << "before: x=" << center_.x << ", y=" << center_.y << std::endl;
        center_.x += p->x;
        center_.y += p->y;
        std::cout << "after: x=" << center_.x << ", y=" << center_.y << std::endl;
    }
};
void drawShapes(const std::list<Shape *> &fig)
{
    std::list<Shape *>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++it)
    {
        (*it)->draw();
    }
}
void moveShapes(const std::list<Shape *> &fig, const std::list<Point*> &points){
    std::list<Shape *>::const_iterator it;
    std::list<Point *>::const_iterator point_iterator = points.begin();
    for (it = fig.begin(); it != fig.end(); ++it)
    {   
        Point* p = *point_iterator;
        (*it)->move(p);
        point_iterator = ++point_iterator;

    }
}
int main(){
    std::list<Shape *> shapes;
    shapes.push_back((Shape *)new Circle);
    shapes.push_back((Shape *)new Square);
    shapes.push_back((Shape *)new Square);
    shapes.push_back((Shape *)new Circle);
    shapes.push_back((Shape *)new Rhomb); //Romb dodan

    std::list<Point *> points = {
        new Point{1, 2},
        new Point{3, 4},
        new Point{5, 6},
        new Point{6, 7},
        new Point{8, 9} //za Romb
    };

    drawShapes(shapes);
    moveShapes(shapes, points);

    for(auto s : shapes){
        delete s;
    }
    for(auto p : points){
        delete p;
    }
    return 0;
}