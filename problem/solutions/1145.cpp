#include<bits/stdc++.h>
using namespace std;
int m,n,a[105][105],dp[105][105],d[4][2]= {{1,0},{0,1},{-1,0},{0,-1}};
int dfs(int x,int y) {
	if(dp[x][y]!=0)return dp[x][y];
	int ans=1;
	for(int i=0; i<4; i++) {
		int xx=x+d[i][0];
		int yy=y+d[i][1];
		if(xx<1||yy<1||xx>m||yy>n)continue;
		if(a[x][y]<=a[xx][yy])continue;
		ans=max(ans,dfs(xx,yy)+1);
	}
	dp[x][y]=ans;
	return ans;
}
int main() {
	cin>>m>>n;
	for(int i=1; i<=m; i++) {
		for(int j=1; j<=n; j++) {
			cin>>a[i][j];
		}
	}
	int maxx=0;
	for(int i=1; i<=m; i++) {
		for(int j=1; j<=n; j++) {
			maxx=max(maxx,dfs(i,j));
		}
	}
	cout<<maxx;
	return 0;
}