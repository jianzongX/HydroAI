#include<bits/stdc++.h>
using namespace std;
int n,m,w[10005],v[10005],f[10000005];
int main(){
	cin>>m>>n;
	for(int i=1;i<=n;i++)cin>>w[i]>>v[i];
	for(int i=1;i<=n;i++){
		for(int j=w[i];j<=m;j++){
			f[j]=max(f[j],f[j-w[i]]+v[i]);
		}		
	}
	cout<<f[m];
	return 0;
}