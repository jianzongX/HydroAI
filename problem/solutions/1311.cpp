#include<bits/stdc++.h>
using namespace std;
int g[10005][10005];
int d[50005];
int dp[50005];
queue<int>q;
int vis[10005][10005];
int main() {
	//freopen("data1.in", "r", stdin);
	int n,m;
	cin>>n>>m;
	for(int i=1; i<=m; i++) {
		int u,v,w;
		cin>>u>>v>>w;
		if(vis[u][v]!=0) {
			g[u][v]=max(g[u][v],w);
		} else {
			vis[u][v]=1;
			g[u][v]=w;
			d[v]++;
		}
		dp[i]=INT_MIN;
	}
	q.push(1);
	dp[1]=0;
	while(!q.empty()) {
		int u = q.front();
		q.pop();
		for(int i=1; i<=n; i++) {
			if(vis[u][i]!=0) {
				d[i]--;
//				cout<<d[i]<<endl;
				if(d[i]==0) {
					q.push(i);
				}
				dp[i]=max(dp[u]+g[u][i],dp[i]);
			}
		}
	}
//	for(int i=1; i<=n; i++) {
//		cout<<dp[i]<<' ';
//	}
    if(dp[n]==INT_MIN)cout<<-1<<endl;
    else cout<<dp[n]<<endl;
	return 0;
}