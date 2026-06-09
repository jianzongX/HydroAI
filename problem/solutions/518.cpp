#include<bits/stdc++.h>
using namespace std;
int f[1005][1005],n,m,a[1005][1005],p[100][100][100];
int main() {
	cin>>n>>m;
	for(int i=1; i<=n; i++) {
		for(int j=1; j<=m; j++) {
			cin>>a[i][j];
		}
	}
	f[0][0]=0;
	for(int i=1; i<=n; i++) {
		for(int j=1; j<=m; j++) {
			for(int k=0; k<=j; k++) {
				if (f[i][j]<f[i-1][j-k]+a[i][k]) {
					f[i][j]=f[i-1][j-k]+a[i][k];
					for(int h=1; h<i; h++)p[i][j][h]=p[i-1][j-k][h];
					p[i][j][i]=k;
				}
			}
		}
	}
	cout<<f[n][m]<<endl;
	for(int i=1; i<=n; i++) {
		cout<<i<<' '<<p[n][m][i]<<endl;
	}
	return 0;
}