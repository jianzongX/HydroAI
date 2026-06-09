#include<bits/stdc++.h>
using namespace std;
int m=1e8;
int n,f;
int dp[2005][2005],r[2005];
int main(){
	cin>>n>>f;
	for(int i=1;i<=n;i++){
		cin>>r[i];
		r[i]%=f;
		dp[i][r[i]]=1;
	}
	for(int i=1;i<=n;i++){
		for(int j=0;j<f;j++){
			dp[i][j]=(dp[i][j]+dp[i-1][j]+dp[i-1][(j-r[i]+f)%f])%m;
		}
	}
	cout<<dp[n][0];
	return 0;
}