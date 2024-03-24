#include <vector>

int getmax(std::vector<int> values){
    int max = values[0];

    for (int i = 1; i < values.size(); i++) {
        if (values[i] > max) max = values[i];
    }
    return max;
}

int isdivbyall(std::vector<int> values, int multiple){
    for(int i = 0; i < values.size(); i++){
            if(multiple % values[i] != 0){
                return false;
            }
        }
    
    return true;
}

int lowestcommonmulitple(std::vector<int> values){
    int multiple = getmax(values);

    while(1){
        if(isdivbyall(values, multiple)){
            return multiple;
        }
        multiple += 1;
    }

} 