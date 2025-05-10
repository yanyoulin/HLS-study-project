#include "dense.h"

void dense(
    data_t input[DIM],
    const data_t weight[FF_DIM][DIM],
    const data_t bias[FF_DIM],
    data_t output[FF_DIM]
) {
#pragma HLS array_partition variable=input complete
#pragma HLS array_partition variable=weight complete dim=2
#pragma HLS array_partition variable=bias complete
#pragma HLS array_partition variable=output complete
#pragma HLS PIPELINE II=1

    for (int i = 0; i < FF_DIM; i++) {
#pragma HLS UNROLL
        data_t acc = bias[i];
        for (int j = 0; j < DIM; j++) {
#pragma HLS UNROLL
            acc += weight[i][j] * input[j];
        }
        output[i] = acc;
    }
}