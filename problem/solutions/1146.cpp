#include<bits/stdc++.h>
using namespace std;
int n,w,ans=100;
int weight[20],c[20];
void dfs(int now,int cnt){
	if(now==n+1){
		ans=min(ans,cnt);
		return;
	}
	for(int i=1;i<=cnt;i++){
		if(cnt>=ans){
			return;
		}
		if(weight[i]+c[now]<=w){
			weight[i]=weight[i]+c[now];
			dfs(now+1,cnt);
			weight[i]=weight[i]-c[now];
		}
	}
	weight[cnt+1]=c[now];
	dfs(now+1,cnt+1);
	weight[cnt+1]=0;
}
int main(){
	cin>>n>>w;
	for(int i=1;i<=n;i++)cin>>c[i];
	dfs(1,0);
	cout<<ans;
	return 0;
}