#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
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

    for (size_t i = 0; i < N; i++) {
        A[i] = (float)i * 0.5f;
        B[i] = (float)i * 0.25f;
    }

    double start = get_time();

    for (int r = 0; r < REPEATS; r++) {

        size_t i = 0;

        // Process eight floats per iteration
        for (; i + 8 <= N; i += 8) {

            __m256 a = _mm256_loadu_ps(&A[i]);
            __m256 b = _mm256_loadu_ps(&B[i]);

            __m256 c = _mm256_add_ps(a, b);

            _mm256_storeu_ps(&C[i], c);
        }

        // Handle remaining elements
        for (; i < N; i++) {
            C[i] = A[i] + B[i];
        }
    }

    double end = get_time();

    double checksum = 0.0;

    for (size_t i = 0; i < N; i++)
        checksum += C[i];

    printf("Dataset size: %zu elements\n", N);
    printf("Repeats: %d\n", REPEATS);
    printf("AVX2 execution time: %.6f seconds\n", end - start);
    printf("Checksum: %.2f\n", checksum);

    free(A);
    free(B);
    free(C);

    return 0;
}
