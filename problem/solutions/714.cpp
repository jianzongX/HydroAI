#include <bits/stdc++.h>
using namespace std;
int n,m;
int v[1005][10]={0},p[1005][10]={0};
int dp[100005]={0};	//只考虑前i个物品，总价格为j的价格与重要度的乘积总和的最大值
int main(){
	cin>>n>>m;
	for(int i=1;i<=m;i++){
		int vv,pp,q;
		cin>>vv>>pp>>q;
		if(!q){
			v[i][0]=vv;
			p[i][0]=pp;
		}else{
			if(v[q][1]==0){
				v[q][1]=vv;
				p[q][1]=pp;
			}else{
				v[q][2]=vv;
				p[q][2]=pp;
			}
		}
	}
	for(int i=1;i<=m;i++){
		if(v[i][0]==0) continue;
		for(int j=n;j>=0;j--){
			if(j>=v[i][0])dp[j]=max(dp[j],dp[j-v[i][0]]+v[i][0]*p[i][0]);//主
			if(j>=v[i][0]+v[i][1])dp[j]=max(dp[j],dp[j-v[i][0]-v[i][1]]+v[i][0]*p[i][0]+v[i][1]*p[i][1]);//主+1
			if(j>=v[i][0]+v[i][2])dp[j]=max(dp[j],dp[j-v[i][0]-v[i][2]]+v[i][0]*p[i][0]+v[i][2]*p[i][2]);//主+2
			if(j>=v[i][0]+v[i][1]+v[i][2])dp[j]=max(dp[j],dp[j-v[i][0]-v[i][1]-v[i][2]]+v[i][0]*p[i][0]+v[i][1]*p[i][1]+v[i][2]*p[i][2]);//主+1+2
		}
	}
//	for(int i=0;i<=n;i++){
//		cout<<dp[i]<<' ';
//	}
	cout<<dp[n];
	return 0;
}