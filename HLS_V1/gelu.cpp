#include "gelu.h"

// Linear approximation of GELU
data_t gelu(data_t x) {
    const data_t a = data_t(0.5);
    const data_t b = data_t(0.79788456);  // sqrt(2/pi)
    const data_t c = data_t(0.035677);    // ≈ 0.044715 * sqrt(2/pi)

    data_t x3 = x * x * x;
    data_t approx = a * x * (1 + b * x + c * x3);
    return approx;
}
