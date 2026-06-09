#include<bits/stdc++.h>
using namespace std;

int g[1005][1005];
int vis[1005];
int s[1005];
int d[1005];
priority_queue<int, vector<int>, greater<int> > q;
int st[1005];

int main() {
	int n,m;
	cin>>n>>m;
	
	memset(g, 0, sizeof(g));
	memset(d, 0, sizeof(d));
	
	for(int i=1; i<=m; i++) {
		int si;
		cin>>si;
		memset(st,0,sizeof(st));
		for(int j=1; j<=si; j++) {
			cin>>s[j];
			st[s[j]]=1;
		}
		for(int j=s[1]; j<=s[si]; j++) {
			if(st[j]==0) {
				for(int k=1; k<=si; k++) {
					int u = j;
					int v = s[k];
					if(g[u][v] == 0) {
						g[u][v] = 1;
						d[v]++;
					}
				}
			}
		}
	}
	for(int i=1;i<=n;i++){
		if(d[i]==0){
			q.push(i);
			vis[i]=1;
		}
	}
	
	while(!q.empty()){
        int u = q.top();
        q.pop();
        for(int v=1; v<=n; v++){
            if(g[u][v] == 1){
                if(vis[v]<vis[u]+1){
                	vis[v]=vis[u]+1;
                }
                d[v]--;
                if(d[v] == 0) {
                	q.push(v);
				}
            }
        }
    }
    int ans=0;
    for(int i=1;i<=n;i++){
    	if(vis[i]>ans){
    		ans=vis[i];
    	}
	}
	cout<<ans;
	return 0;
}