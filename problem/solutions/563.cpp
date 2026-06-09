#include<bits/stdc++.h>
using namespace std;
long long n, a[100005], L[100005], R[100005], i = 1, j = 1, ans = 0;
void MERGE(long long l, long long q, long long r) {
	long long n1 = q - l + 1, n2 = r - q;
	for (i = 1; i <= n1; i++) {
		L[i] = a[l + i - 1];
	}
	for (j = 1; j <= n2; j++) {
		R[j] = a[q + j];
	}
	L[i] = 0x7f7f7f7f, R[j] = 0x7f7f7f7f;
	i = 1, j = 1;
	for (long long k = l; k <= r; k++) {
		if (L[i] <= R[j]) {
			a[k] = L[i];
			i++;
		} else {
			a[k] = R[j];
			j++;
			ans += n1 - i + 1;
		}
	}
	return;
}
void MERGE_SORT(long long l, long long r) {
	if (l < r) {
		long long q = (l + r) / 2;
		MERGE_SORT(l, q);
		MERGE_SORT(q + 1, r);
		MERGE(l, q, r);
	}
	return;
}
int main() {
	cin >> n;
	for (long long k = 0; k < n; k++) {
		cin >> a[k];
	}
	MERGE_SORT(0, n - 1);
	cout << ans;
	return 0;
}