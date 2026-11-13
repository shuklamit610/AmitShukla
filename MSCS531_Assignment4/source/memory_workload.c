#include <stdio.h>
#include <stdlib.h>

#define SIZE 100000
#define ITERATIONS 5

int main() {
    static int data[SIZE];
    long long sum = 0;

    printf("Memory Intensive Workload\n");

    // Initialize the array
    for (int i = 0; i < SIZE; i++) {
        data[i] = i;
    }

    // Repeated memory reads and writes
    for (int j = 0; j < ITERATIONS; j++) {
        for (int i = 0; i < SIZE; i++) {
            data[i] = data[i] + 1;
            sum += data[i];
        }
    }

    printf("Array Size = %d\n", SIZE);
    printf("Iterations = %d\n", ITERATIONS);
    printf("Result = %lld\n", sum);

    return 0;
}
