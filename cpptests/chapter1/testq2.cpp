#include<iostream>
#include"q2.h"

int main(int argc, char* argv[]){
    std::cout << "Enter two numbers: " << std::endl;
    int a, b;
    std::cout << "Enter first number: " << std::endl;
    std::cin >>a;
    std::cout << "Enter second number: " << std::endl;
    std::cin >>b;

    std::cout << "The highest common denominator is " << largestdenominator(a, b)<< std::endl;
}