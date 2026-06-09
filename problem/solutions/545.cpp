#include<bits/stdc++.h>
using namespace std;
int dp[1005]={0},n;
int main(){
    cin>>n;
    int a[4] = {10, 20, 50, 100};
    dp[0]=1;
    for (int j = 0; j < 4; j++) {
        int t = a[j];
        for (int i = t; i <= n; i++) {
            dp[i] += dp[i - t];
        }
    }
    cout << dp[n];
    return 0;
}