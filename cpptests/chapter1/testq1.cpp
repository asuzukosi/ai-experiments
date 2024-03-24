#include<iostream>
#include"q1.h"



int main(int argc, char* argv[]){
   int stop; 
   std::cout << "Enter a stop point" << std::endl;
   std::cin >> stop;

   int sum = 0;

   for(int i = 3; i <=stop; i++){
        if (divby3and5(i)){
            sum += i;
        }
   }

   std::cout << "The sum of the numbers is " << sum << std::endl;
   return 0;
}