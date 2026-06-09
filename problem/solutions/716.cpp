#include <bits/stdc++.h>
using namespace std;
int dp[10005], p[105][105];//包容量为i时在明天买出能获得的最大正收益 
int main() {
    int t, n, m, ans;
    cin>>t>>n>>m;
    for (int i = 1; i <= t; i++) {
        for (int j = 1; j <= n; j++) {
            cin>>p[i][j];
        }
    }
    ans = m;
    for (int i = 1; i < t; i++) {
        dp[ans] = ans;
        for (int j = 1; j <= n; j++) {
            for (int k = ans; k >= p[i][j]; k--) {
                dp[k - p[i][j]] = max(dp[k - p[i][j]], dp[k] + p[i + 1][j] - p[i][j]);
            }
        }
        int maxx=0;
        for (int j = 0; j <= ans; ++j) {
            maxx=max(maxx,dp[j]);
        }
        ans=maxx;
    }
    cout<<ans<<endl;
    return 0;
}