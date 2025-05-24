#include "top.h"
#include <iostream>

int main() {
    data_t input[DIM] = {1.0, 2.0, 3.0, 4.0};
    data_t output[FF_DIM];

    mlp_inference(input, output);

    std::cout << "Output:\n";
    for (int i = 0; i < FF_DIM; i++) {
        std::cout << output[i].to_double() << " ";
    }
    std::cout << std::endl;

    return 0;
}
