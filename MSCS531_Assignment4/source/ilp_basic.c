
#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;
    int c = 30;

    int x = a + b;
    int y = b + c;
    int z = x * y;

    int result = 0;

    for (int i = 0; i < 100; i++) {
        result += i;
    }

    printf("ILP Basic Workload\n");
    printf("X = %d\n", x);
    printf("Y = %d\n", y);
    printf("Z = %d\n", z);
    printf("Result = %d\n", result);

    return 0;
}
