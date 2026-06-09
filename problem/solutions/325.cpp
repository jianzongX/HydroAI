#include <stdio.h>
int n, a, b;
int main(void) {
    scanf("%d %d %d", &n, &a, &b);
    int c, d; double x = 1.0 * b / a, y;
    while (n-- != 1) {
        scanf("%d %d", &c, &d);
        y = 1.0 * d / c;
        if(y - x >= 0.05) puts("better");
        else
            if(x - y >= 0.05) puts("worse");
            else puts("same");
    }
    return 0;
}