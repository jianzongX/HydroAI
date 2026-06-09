#include<bits/stdc++.h>
using namespace std;
vector<int> g[100005];
int h[100005],v[100005],k,n,m;
void dfs(int u){
    v[u]=1;
    for(int i=0;i<g[u].size();i++){ 
        int k=g[u][i];
        if(v[k]==0)dfs(k);
    }
}
int main() {
    cin>>k>>n>>m;
    vector<int> f(10005); 
    for(int i=1;i<=k;i++)cin>>f[i];
    int a,b;
    for(int i=1;i<=m;i++){
        cin>>a>>b;
        g[a].push_back(b);
    }
    for(int i=1;i<=n;i++)h[i]=1;
    for(int i=1;i<=k;i++){
        int x=f[i];
        memset(v,0,sizeof(v));
        dfs(x);
        for(int j=1;j<=n;j++){
        	if(h[j]==1&&v[j]==1)h[j]=1;
			else h[j]=0;
        }
    }
    int ans=0;
    for(int i=1;i<=n;i++)if(h[i])ans++;
    cout<<ans;
    return 0;
}