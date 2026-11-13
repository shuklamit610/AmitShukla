#include <stdio.h>

int main() {
    double a = 1.25, b = 2.50;
    double result = 0.0;

    for (int i = 0; i < 100000; i++) {
        result += (a * b) + (a / b);
        a += 0.00001;
    }

    printf("Floating Point Workload\n");
    printf("Result = %.4f\n", result);

    return 0;
}
