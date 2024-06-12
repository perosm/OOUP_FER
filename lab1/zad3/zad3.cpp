#include <iostream>

// https://en.wikipedia.org/wiki/Data_structure_alignment#Data_structure_padding

class CoolClass{
public: 
  //4B za vptr + 8B za alignment pointera
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_; //4B
};
class PlainOldClass{
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_; //4B
};

int main(){
    std::cout << sizeof(CoolClass) << std::endl; // 16B
    std::cout << sizeof(PlainOldClass) << std::endl; // 4B

    return 0;
}