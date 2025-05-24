#ifndef DENSE_H
#define DENSE_H

#include "common.h"

void dense(
    data_t input[DIM],
    const data_t weight[FF_DIM][DIM],
    const data_t bias[FF_DIM],
    data_t output[FF_DIM]
);

#endif