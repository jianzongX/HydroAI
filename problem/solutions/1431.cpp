#include <bits/stdc++.h>
using namespace std;

const int MOD = 998244353;

long long dp[5005] = {0};
long long n;
long long a[5005];

long long power(long long a, long long b) {
    long long res = 1;
    while (b) {
        if (b & 1) res = res * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}

int main() {
    freopen("polygon.in", "r", stdin);
    freopen("polygon.out", "w", stdout);
    
    cin >> n;
    for (long long i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    sort(a, a + n);
    
    dp[0] = 1;
    long long ans = 0;
    
    for (long long i = 0; i < n; i++) {
        for (long long j = 0; j <= a[i]; j++) {
            ans = (ans + dp[j]) % MOD;
        }
        
        for (long long j = 5000; j >= a[i]; j--) {
            dp[j] = (dp[j] + dp[j - a[i]]) % MOD;
        }
    }
    
    long long total = (power(2, n) - 1 + MOD) % MOD;
    long long invalid = (n + n * (n - 1) / 2) % MOD;
    invalid = (invalid + ans) % MOD;
    
    ans = (total - invalid + MOD) % MOD;
    cout << ans << endl;
    return 0;
}