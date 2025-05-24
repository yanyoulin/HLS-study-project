#include "softmax.h"
#include <hls_math.h>

void softmax(data_t input[DIM], data_t output[DIM]) {
#pragma HLS array_partition variable=input complete
#pragma HLS array_partition variable=output complete

    data_t sum = 0;
    data_t exp_values[DIM];
#pragma HLS array_partition variable=exp_values complete

    for (int i = 0; i < DIM; ++i) {
#pragma HLS UNROLL
        exp_values[i] = hls::exp(input[i]);
        sum += exp_values[i];
    }

    for (int i = 0; i < DIM; ++i) {
#pragma HLS UNROLL
        output[i] = exp_values[i] / sum;
    }
}
