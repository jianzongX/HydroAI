#include <bits/stdc++.h>
using namespace std;
bool vis[1005][1005];
char ch[1005][1005];
const int dx[]={0,1,0,-1},dy[]={1,0,-1,0};
void solve() {
	int n,m,k,x0,y0,d0;
	memset(vis,0,sizeof(vis));
	cin >> n >> m >> k;
	cin >> x0 >> y0 >> d0;
	for (int i=1;i<=n;i++) {
		char s[1005];
		cin >> s;
		for (int j=1;j<=m;j++)
			ch[i][j]=s[j-1];
	}
	vis[x0][y0]=true;
	for (int i=1;i<=k;i++) {
		int x1=x0+dx[d0],y1=y0+dy[d0];
		if (1<=x1 && x1<=n && 1<=y1 && y1<=m && ch[x1][y1]=='.') {
			x0=x1;
			y0=y1;
		}
		else
			d0=(d0+1)%4;
		vis[x0][y0]=true;
	}
	int ans=0;
	for (int i=1;i<=n;i++) {
		for (int j=1;j<=m;j++)
			ans+=vis[i][j];
	}
	cout << ans << endl;
}
int main() {
	int T;
	cin >> T;
	while (T--) {
		solve();
	}
}