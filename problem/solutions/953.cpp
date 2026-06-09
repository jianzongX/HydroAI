#include <bits/stdc++.h>
using namespace std;
int n,m,ans;
char c;
int main()
{
    cin >> n;
    while(~scanf("%c%d",&c,&m))
    {
        if(c == '+') ans += n,n = m;
        else if(c == '*') n *= m;
        ans %= 10000;
        n %= 10000;
    }
    cout << (ans + n) % 10000;
}