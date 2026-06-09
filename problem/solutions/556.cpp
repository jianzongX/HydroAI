#include <bits/stdc++.h>
using namespace std;
int n, k;
int main() {
    cin >> n >> k;
    int dp[1005][1005];
    dp[0][0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= k; j++) {
            if (i >= j) {
                dp[i][j] = dp[i - 1][j - 1] + dp[i - j][j];
            }
        }
    }
    cout << dp[n][k] << endl;
    return 0;
}