#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    int thread_id;
    int num_threads;
    long n;
    double a;
    double *x;
    double *y;
} ThreadArgs;

static void *daxpy_worker(void *arg)
{
    ThreadArgs *args = (ThreadArgs *)arg;

    long start = args->n * args->thread_id / args->num_threads;
    long end   = args->n * (args->thread_id + 1) / args->num_threads;

    for (long i = start; i < end; i++) {
        args->y[i] = args->a * args->x[i] + args->y[i];
    }

    return NULL;
}

static double seconds(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

int main(int argc, char **argv)
{
    long n = (argc > 1) ? atol(argv[1]) : 100000;
    int num_threads = (argc > 2) ? atoi(argv[2]) : 1;
    const double a = 2.5;

    if (n <= 0 || num_threads <= 0) {
        fprintf(stderr, "Usage: %s [vector_size] [threads]\n", argv[0]);
        return 1;
    }

    double *x = malloc((size_t)n * sizeof(double));
    double *y = malloc((size_t)n * sizeof(double));
    pthread_t *threads = malloc((size_t)num_threads * sizeof(pthread_t));
    ThreadArgs *args = malloc((size_t)num_threads * sizeof(ThreadArgs));

    if (!x || !y || !threads || !args) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    for (long i = 0; i < n; i++) {
        x[i] = 1.0 + (i % 100) * 0.01;
        y[i] = 2.0;
    }

    double start_time = seconds();

    for (int t = 1; t < num_threads; t++) {
        args[t] = (ThreadArgs){t, num_threads, n, a, x, y};
        if (pthread_create(&threads[t], NULL, daxpy_worker, &args[t]) != 0) {
            perror("pthread_create");
            return 1;
        }
    }

    args[0] = (ThreadArgs){0, num_threads, n, a, x, y};
    daxpy_worker(&args[0]);

    for (int t = 1; t < num_threads; t++) {
        pthread_join(threads[t], NULL);
    }

    double elapsed = seconds() - start_time;

    double checksum = 0.0;
    for (long i = 0; i < n; i++) {
        checksum += y[i];
    }

    printf("DAXPY n=%ld threads=%d elapsed_seconds=%.6f checksum=%.6f\n",
           n, num_threads, elapsed, checksum);

    free(x);
    free(y);
    free(threads);
    free(args);
    return 0;
}
