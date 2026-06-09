#include<bits/stdc++.h>
using namespace std;
int n,m;
int d[10005],c[10005];
int dp[10005][10005];//dp(i,j)表示前i项工作花费j元能完成的最多工作数
void kp(int l,int r) {
	if(l>=r)return;
	int i=l,j=r,x=c[l],y=d[l];
	while(i!=j) {
		while(i<j&&c[j]>x)j--;
		if(i<j) {
			c[i]=c[j];
			d[i]=d[j];
			i++;
		}
		while(i<j&&c[i]<=x)i++;
		if(i<j) {
			c[j]=c[i];
			d[j]=d[i];
			j--;
		}
	}
	c[i]=x;
	d[i]=y;
	kp(l,i-1);
	kp(i+1,r);
}
int main() {
	cin>>n>>m;
	for(int i=1; i<=n; i++) {
		cin>>d[i];
	}
	for(int i=1; i<=n; i++) {
		cin>>c[i];
	}
	kp(1,n);
	
	for(int i=1;i<=n;i++){
		for(int j=0;j<=m;j++){
			if(j-d[i]>=0)dp[i][j]=max(dp[i-1][j],dp[i-1][j-d[i]+c[i]]+1);
			else dp[i][j]=dp[i-1][j];
		}
	}
	int maxx=0;
	for(int i=0;i<=m;i++){
		maxx=max(dp[n][i],maxx);
	}
	cout<<maxx;
	return 0;
}