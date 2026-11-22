
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define REPEATS 1

double get_time()
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);

    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main(int argc, char *argv[])
{
    size_t N = 1000000;

    if (argc > 1)
        N = strtoull(argv[1], NULL, 10);

    float *A, *B, *C;

    if (posix_memalign((void **)&A, 32, N * sizeof(float)) ||
        posix_memalign((void **)&B, 32, N * sizeof(float)) ||
        posix_memalign((void **)&C, 32, N * sizeof(float))) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Initialize arrays
    for (size_t i = 0; i < N; i++) {
        A[i] = (float)i * 0.5f;
        B[i] = (float)i * 0.25f;
    }

    double start = get_time();

    // Vector addition
    for (int r = 0; r < REPEATS; r++) {
        for (size_t i = 0; i < N; i++) {
            C[i] = A[i] + B[i];
        }
    }

    double end = get_time();

    // Calculate checksum to verify results
    double checksum = 0.0;

    for (size_t i = 0; i < N; i++)
        checksum += C[i];

    printf("Dataset size: %zu elements\n", N);
    printf("Repeats: %d\n", REPEATS);
    printf("Execution time: %.6f seconds\n", end - start);
    printf("Checksum: %.2f\n", checksum);

    free(A);
    free(B);
    free(C);

    return 0;
}
