#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;



int dp[1001][1001];

int main() {
    int N, M, K;
    cin >> N >> M >> K;

    memset(dp, -1, sizeof(dp));
    dp[0][0] = 0;

    for (int k = 0; k < K; ++k) {
        int a, b;
        cin >> a >> b;

        for (int i = N; i >= a; --i) {
            for (int j = M - 1; j >= b; --j) {
                if (dp[i - a][j - b] != -1) {
                    dp[i][j] = max(dp[i][j], dp[i - a][j - b] + 1);
                }
            }
        }
    }

    int max_c = 0, min_hurt = 0;
    for (int i = 0; i <= N; ++i) {
        for (int j = 0; j < M; ++j) {
            if (dp[i][j] > max_c) {
                max_c = dp[i][j];
                min_hurt = j;
            } else if (dp[i][j] == max_c && j < min_hurt) {
                min_hurt = j;
            }
        }
    }

    cout << max_c << " " << (M - min_hurt) << endl;

    return 0;
}