#include<bits/stdc++.h>
using namespace std;
int main() {
	int a[105][105],f[105][105]={0},r,n,m;
	cin>>r;
	for(int i=1; i<=r; i++) {
		cin>>n>>m;
		for(int j=1; j<=n; j++) {
			for(int k=1; k<=m; k++) {
				cin>>a[j][k];
				f[i][j]=0;
			}
		}
		for(int i=1; i<=n; i++) {
			for(int j=1; j<=m; j++) {
				f[i][j]=max(f[i-1][j],f[i][j-1])+a[i][j];
			}
		}
		cout<<f[n][m]<<endl;
	}
	return 0;
}