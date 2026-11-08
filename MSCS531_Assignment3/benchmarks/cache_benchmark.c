
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define ARRAY_SIZE (2 * 1024 * 1024)
#define ITERATIONS 10

int main(void)
{
    volatile uint32_t *array =
        malloc(ARRAY_SIZE * sizeof(uint32_t));

    if (array == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Initialize the array.
    for (size_t i = 0; i < ARRAY_SIZE; i++) {
        array[i] = (uint32_t)i;
    }

    // Repeatedly access the array to exercise the cache.
    uint64_t total = 0;

    for (int j = 0; j < ITERATIONS; j++) {
        for (size_t i = 0; i < ARRAY_SIZE; i++) {
            total += array[i];
        }
    }

    printf("Cache benchmark completed.\n");
    printf("Array elements: %d\n", ARRAY_SIZE);
    printf("Iterations: %d\n", ITERATIONS);
    printf("Checksum: %llu\n", (unsigned long long)total);

    free((void *)array);
    return 0;
}
