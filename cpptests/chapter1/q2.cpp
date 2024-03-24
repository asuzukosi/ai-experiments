
int smallest(int a, int b){
    if (a < b) return a;
    else return b;
}
 

int largestdenominator(int a, int b){
    int denominator = 1;
    for(int i = 1; i <= smallest(a, b); i++){
        if(a % i == 0 && b % i == 0){
            denominator = i;
        }
    }
    return denominator;
}