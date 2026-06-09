#include <bits/stdc++.h>
using namespace std;
int main(){
    int n;
    scanf("%d", &n);
    double sum = 0;
    for (int i = 1; i <= n; i++){
        double x, y;//注意是 double 类型
        int p;
        scanf("%lf%lf%d", &x, &y, &p);
        double dis = sqrt(x * x + y * y);
        sum += dis / 50 + p + dis / 50 + p * 0.5;
        //船往返的时间总和
    }
    printf("%d\n", int(ceil(sum)));//向上取整函数
    return 0;
}