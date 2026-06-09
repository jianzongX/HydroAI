#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m, L;
    cin >> n >> m >> L;
    int movies[100][2];
    for (int i = 0; i < n; ++i) {
        cin >> movies[i][0] >> movies[i][1];
    }

    int dp[101][101][1001];
    for (int i = 0; i <= n; ++i) {
        for (int j = 0; j <= m; ++j) {
            for (int k = 0; k <= L; ++k) {
                dp[i][j][k] = -1;
            }
        }
    }
    dp[0][0][0] = 0;

    for (int i = 1; i <= n; ++i) {
        int ti = movies[i-1][0];
        int vi = movies[i-1][1];
        for (int j = 0; j <= m; ++j) {
            for (int k = 0; k <= L; ++k) {
                if (dp[i-1][j][k] != -1) {
                    dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k]);
                }
                if (j >= 1 && k >= ti && dp[i-1][j-1][k-ti] != -1) {
                    dp[i][j][k] = max(dp[i][j][k], dp[i-1][j-1][k-ti] + vi);
                }
            }
        }
    }

    int mv = -1;
    for (int k = 0; k <= L; ++k) {
        if (dp[n][m][k] > mv) {
            mv = dp[n][m][k];
        }
    }

    if (mv == -1) {
        cout << 0 << endl;
    } else {
        cout << mv << endl;
    }

    return 0;
}