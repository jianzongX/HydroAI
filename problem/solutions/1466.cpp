#include <bits/stdc++.h>
using namespace std;
#define int long long
const int MAXN=2e5+5 ;
int dp[MAXN][3],a[MAXN],b[MAXN];
int ans=1e18;
signed main(){
	int n;
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a[i];
		b[i]=a[i]-a[i-1];
	} 
	for(int i=2;i<=n;i++){
		if(b[i]>0){
			dp[i][0]=dp[i-1][0];
		}
		else {
			dp[i][0]=dp[i-1][0]-b[i]+1;
		}
	}
	dp[n][1]=0;
	for(int i=n-1;i>=1;i--){
		if(b[i+1]<0){
			dp[i][1]=dp[i+1][1];
		}
		else {
			dp[i][1]=dp[i+1][1]+b[i+1]+1;
		}
	}
	for(int i=1;i<=n;i++){
		ans=min(ans,max(dp[i][0],dp[i][1]));
	}
	cout<<ans;
}