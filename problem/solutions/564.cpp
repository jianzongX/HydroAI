#include<bits/stdc++.h>
using namespace std;
unsigned long long f[100],g[100];
int main(){
	int x,y,z;
	cin>>x>>y>>z;
	for(int i=1;i<=x;i++){
		f[i]=1;
		g[i]=0;
	}
	for(int i=x+1;i<=z+1;i++){
		g[i]=f[i-x]*y;
		f[i]=f[i-1]+g[i-2];
	}
	cout<<f[z+1];
    return 0;	
}