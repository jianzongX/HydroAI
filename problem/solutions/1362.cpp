#include<bits/stdc++.h>
using namespace std;
vector<int> g[100005];
int vis[100005][2];
int n,m;
void dfs(int i)
{
	cout<<i<<" ";
	vis[i][0]=1;
	for(int j=0;j<g[i].size();j++){
		if(!vis[g[i][j]][0]){
			dfs(g[i][j]);
		}
	}
}
void bfs(int i)
{
	vis[i][1]=1;
	queue<int>q;
	q.push(i);
	while(!q.empty()){
		int n=q.front();
		cout<<n<<" ";
		for(int j=0;j<g[n].size();j++){
			if(!vis[g[n][j]][1]){
				q.push(g[n][j]);
				vis[g[n][j]][1]=1;
			}
		}
		q.pop();
	}
}
int main(){
	cin>>n>>m;
	for(int i=1;i<=m;i++){
		int u,v;
		cin>>u>>v;
		g[u].push_back(v);
    }
	for(int i=1;i<=n;i++)sort(g[i].begin(),g[i].end());
	for(int i=1;i<=n;i++)if(vis[i][0]==0)dfs(i);
	cout<<endl;
	for(int i=1;i<=n;i++)if(vis[i][1]==0)bfs(i);
	return 0;
 }