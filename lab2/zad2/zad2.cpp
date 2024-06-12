#include <iostream>
#include <stdio.h>
#include <vector>
#include <set>
#include <string>
#include <string.h>

//using namespace std;

int gt_int(int a, int b){
    return (a > b) ? 1 : 0; //return 1 if the first argument is > the second
}

int gt_str(std::string a, std::string b){
    return a.compare(b) > 0 ? 1 : 0;
}
template <typename Iterator, typename Predicate> Iterator mymax(Iterator first, Iterator last, Predicate pred){
    Iterator max = first;
    while(first != last){
        max = pred(*first, *max) == 1 ? first : max;
        ++first;
    }
    
    return max;
}

int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
//ostali standardni spremnici
std::vector<int> vec_int({1, 3, 5, 7, 4, 6, 9, 2, 0});
std::set<int> set_int({1, 3, 5, 7, 4, 6, 9, 2, 0});
//sa stringon
std::string arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",  
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };
std::vector<std::string> vec_str({
        "Gle", "malu", "vocku", "poslije", "kise",  
        "Puna", "je", "kapi", "pa", "ih", "njise"
    });
std::set<std::string> set_str{
        "Gle", "malu", "vocku", "poslije", "kise",  
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };
int main(){
    const int* maxint = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int); //*arr_int -> prvi element
    std::cout << *maxint <<"\n";
    std::vector<int>::iterator maxint2 = mymax(vec_int.begin(), vec_int.end(), gt_int);
    std::cout <<*maxint2 <<"\n";
    std::set<int>::iterator  maxint3 = mymax(set_int.begin(), set_int.end(), gt_int);
    std::cout << *maxint3 <<"\n";
    std::string* maxstr = mymax(&arr_str[0], &arr_str[sizeof(arr_str)/sizeof(*arr_str)], gt_str); //*arr_str -> prvi element
    std::cout << *maxstr <<"\n";
    std::vector<std::string>::iterator maxstr2 = mymax(vec_str.begin(), vec_str.end(), gt_str);
    std::cout << *maxstr2 <<"\n";
    std::set<std::string>::iterator maxstr3 = mymax(set_str.begin(), set_str.end(), gt_str);
    std::cout << *maxstr3 <<"\n";

    return 0;
}       