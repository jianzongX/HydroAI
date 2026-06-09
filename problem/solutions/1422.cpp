#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;
string a, b;  
string c, d;  
long long len;
long long dp[100005][2];  

int main() {
    freopen("bit.in", "r", stdin);
    freopen("bit.out", "w", stdout);
    cin >> c >> d;
    for (long long i = 0; i < c.size(); i++) {
        a += c[c.size() - 1 - i];
    }
    for (long long i = 0; i < d.size(); i++) {
        b += d[d.size() - 1 - i];
    }
    len = max(c.size(), d.size());
    dp[0][0] = 1;
    dp[0][1] = 0;
    while (c.size() < len) c += '0';
    while (d.size() < len) d += '0';
    for (long long i = 0; i < len; i++) {
        for (long long j = 0; j <= 1; j++) {
            if (dp[i][j] == 0) continue;
            long long sum = int(a[i]-'0')+int(b[i]-'0')+ j;
            if (sum < 10) {
                dp[i+1][0] = (dp[i+1][0] + dp[i][j]) % MOD;
            } else {
                dp[i+1][0] = (dp[i+1][0] + dp[i][j]) % MOD;
                dp[i+1][1] = (dp[i+1][1] + dp[i][j]) % MOD;
            }
        }
    }
    cout << (dp[len][0]+dp[len][1] )%MOD<< endl;
    return 0;
}