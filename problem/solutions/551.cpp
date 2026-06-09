#include<bits/stdc++.h>
using namespace std;
int n,k,f[105][105],a[105];
int main(){
	cin>>n>>k;
	memset(f,0xcfcfcfcf,sizeof(f));
	for(int i=1;i<=n;i++){
		cin>>a[i];
		f[i][0]=0;
	}
	f[0][0]=0;
	for(int i=1;i<=n;i++){
		for(int j=0;j<=k-1;j++){
			f[i][j]=max(f[i-1][j],f[i-1][(j-a[i]+k*1000000)%k]+a[i]);
//			cout<<i<<' '<<j<<"-----"<<f[i][j]<<endl;
		}
	}
	cout<<f[n][0];
	return 0;
}