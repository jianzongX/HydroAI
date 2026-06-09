#include <bits/stdc++.h>
using namespace std;
int ans[1005],a[1005],b[1005][1005],c[1005],v,g,minn=100000000;
int f(int t, int s) {
    if (t > g) {
        for (int i = 1; i <= v; i++) {
            int sum = 0;
            for (int j = 1; j <= s; j++)
                sum += b[c[j]][i];
            if (sum < a[i]) return 0;
        }
        if (s < minn) {
            minn = s;
            for (int i = 1; i <= minn; i++) {
                ans[i] = c[i];
            }
        }
        return 1;
    }
    c[s + 1] = t;
    f(t + 1, s + 1);
    c[s + 1] = 0;
    f(t + 1, s);
    return 0;
}
int main() {
	cin>>v;
	for(int i=1; i<=v; i++)cin>>a[i];
	cin>>g;
	for(int i=1; i<=g; i++)for(int j=1; j<=v; j++)cin>>b[i][j];
	f(1,0);
	cout<<minn<<' ';
	for(int i=1; i<=minn; i++)cout<<ans[i]<<' ';
	return 0;
}