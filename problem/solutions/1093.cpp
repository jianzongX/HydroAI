#include <bits/stdc++.h>
using namespace std;
long long m,n,dp[25][2000005]={0},w[25],c[25];
int main() {
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>w[i];
	}
	for(int i=1;i<=n;i++){
		cin>>c[i];
	}
	for(int i=1;i<=n;i++){
		for(int j=0;j<=m;j++){
			if(j<w[i]) dp[i][j]=dp[i-1][j];
			else dp[i][j]=max(dp[i-1][j],dp[i-1][j-w[i]]+c[i]);
		}
	}
    cout<<dp[n][m];
	return 0;
}