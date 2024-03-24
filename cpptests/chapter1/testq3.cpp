#include <iostream>
#include <vector>
#include"q3.h"

int main(int argc, char* argv[]){
    
    std::vector<int> numbers;
    int input;

    std::cout<< "Enter numbers, press non numeric key to stop"<<std::endl;

    while(std::cin >> input){
        numbers.push_back(input);
    }

    std::cout<<"The lowest common multiple is "<< lowestcommonmulitple(numbers) << std::endl;
    
}