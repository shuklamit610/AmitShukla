#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

static double checksum(const float *a, size_t n) {
    double sum = 0.0;
    for (size_t i = 0; i < n; i++) {
        sum += a[i];
    }
    return sum;
}

int main(int argc, char **argv) {
    size_t n = (argc > 1) ? strtoull(argv[1], NULL, 10) : 10000000;

    float *a = malloc(n * sizeof(float));
    float *b = malloc(n * sizeof(float));
    float *c = malloc(n * sizeof(float));

    if (!a || !b || !c) {
        fprintf(stderr, "Memory allocation failed for %zu elements.\n", n);
        free(a);
        free(b);
        free(c);
        return 1;
    }

    for (size_t i = 0; i < n; i++) {
        a[i] = (float)(i % 100) * 0.5f;
        b[i] = (float)(i % 50) * 0.25f;
    }

    double start, end;

    start = omp_get_wtime();
    for (size_t i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
    end = omp_get_wtime();
    printf("Sequential:          %.6f s\n", end - start);
    printf("Sequential checksum: %.2f\n", checksum(c, n));

    start = omp_get_wtime();
    #pragma omp parallel for
    for (size_t i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
    end = omp_get_wtime();
    printf("OpenMP parallel for: %.6f s\n", end - start);
    printf("Parallel checksum:   %.2f\n", checksum(c, n));

    start = omp_get_wtime();
    #pragma omp parallel for simd
    for (size_t i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
    end = omp_get_wtime();
    printf("OpenMP for simd:      %.6f s\n", end - start);
    printf("For-simd checksum:    %.2f\n", checksum(c, n));

    free(a);
    free(b);
    free(c);
    return 0;
}
