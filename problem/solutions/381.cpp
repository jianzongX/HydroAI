#include<bits/stdc++.h>
using namespace std;
int a[105][105],b[105][105],n,m;
int main(){
	cin>>n>>m;
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			cin>>a[i][j];
		}
	}
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			b[i][j]=a[i][j];
		}
	}
	for(int i=1;i<n-1;i++){
		for(int j=1;j<m-1;j++){
			b[i][j]=round((a[i][j]+a[i-1][j]+a[i+1][j]+a[i][j-1]+a[i][j+1])/5.0);
		}
	}
	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			cout<<b[i][j]<<" ";
		}
		cout<<endl;
	}
	return 0;
}