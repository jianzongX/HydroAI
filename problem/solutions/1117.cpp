#include <bits/stdc++.h>

using namespace std;

using LL = long long;

const int N = 1e5 + 10;

int v[N], a[N];
int n, d;
int main() {
    scanf("%d%d", &n, &d);
    for (int i = 1; i < n; i++) scanf("%d", &v[i]);
    int mi = INT_MAX;
    LL ans = 0, s = 0;
    for (int i = 1; i < n; i++) {
        scanf("%d", &a[i]);
        s += v[i];
        mi = min(mi, a[i]);
        if (s > 0) {
            ans += (s + d - 1) / d * mi;
            s -= (s + d - 1) / d * d;
        }
    }
    printf("%lld\n", ans);
    return 0;
}