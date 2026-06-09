#include<bits/stdc++.h>
using namespace std;
int m, n;
int w[35], c[35], p[35];
int dp[205]={0};//重量为i的最大价值 
int main() {
    cin >> m >> n;
    for (int i = 1; i <= n; i++) {
        cin >> w[i] >> c[i] >> p[i];
    }
    for (int i = 1; i <= n; i++) {
        if (p[i] == 0) {
            for (int j = w[i]; j <= m; j++) {
                dp[j] = max(dp[j], dp[j - w[i]] + c[i]);
            }
        } else {
            for (int j = m; j >= w[i]; j--) {
                for (int k = 1; k <= p[i] && k * w[i] <= j; k++) {
                    dp[j] = max(dp[j], dp[j - k * w[i]] + k * c[i]);
                }
            }
        }
    }
    cout<<dp[m];
    return 0;
}