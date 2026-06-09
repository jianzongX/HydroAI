#include <iostream>
#include <climits>
using namespace std;

const int MAX_N = 205;
const int MAX_K = 20005;

int main() {
    int n;
    cin >> n;

    int b[MAX_N];
    for (int i = 0; i < n; ++i) {
        cin >> b[i];
    }

    int c[MAX_N];
    for (int i = 0; i < n; ++i) {
        cin >> c[i];
    }

    int k;
    cin >> k;

    int dp[MAX_K];
    for (int i = 0; i <= k; ++i) {
        dp[i] = INT_MAX;
    }
    dp[0] = 0;

    for (int i = 0; i < n; ++i) {
        for (int j = 1; j <= c[i]; j *= 2) {
            for (int m = k; m >= j * b[i]; --m) {
                if (dp[m - j * b[i]] != INT_MAX) {
                    dp[m] = min(dp[m], dp[m - j * b[i]] + j);
                }
            }
            c[i] -= j;
        }
        if (c[i] > 0) {
            for (int m = k; m >= c[i] * b[i]; --m) {
                if (dp[m - c[i] * b[i]] != INT_MAX) {
                    dp[m] = min(dp[m], dp[m - c[i] * b[i]] + c[i]);
                }
            }
        }
    }

    if (dp[k] == INT_MAX) {
        cout << -1 << endl;
    } else {
        cout << dp[k] << endl;
    }

    return 0;
}