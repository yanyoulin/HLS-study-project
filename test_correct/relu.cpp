#include "relu.h"

void relu(data_t input[DIM], data_t output[DIM]) {
#pragma HLS array_partition variable=input complete
#pragma HLS array_partition variable=output complete

    for (int i = 0; i < DIM; i++) {
#pragma HLS UNROLL
        output[i] = (input[i] > 0) ? input[i] : data_t(0);
    }
}
