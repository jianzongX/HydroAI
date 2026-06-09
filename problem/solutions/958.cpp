#include<bits/stdc++.h>
using namespace std;
int main() {
	int n, m;
	cin >> n >> m;
	int a;
	int dp[105] = {0};
	dp[0] = 1;
	for (int i = 1; i <= n; ++i) {
		cin >> a;
		for (int j = m; j >= 0; --j) {
			int sum = 0;
			for (int k = 1; k <= min(a, j); ++k) {
				sum = (sum + dp[j - k]) % 1000007;
			}
			dp[j] = (dp[j] + sum) % 1000007;
		}
	}
	cout << dp[m] << endl;
	return 0;
}