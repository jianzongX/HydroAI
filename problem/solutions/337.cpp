//方法一
#include <iostream>
#include <cstdio>
using namespace std;
  
long long a, b, s = 1;
 
int main()
{
    cin >> a >> b;
    for(int i = 0;i < b;++i)
        s *= a, s %= 1000; //每乘一次模一次1000
    printf("%03lld", s); //补满3位的0
    return 0;
}