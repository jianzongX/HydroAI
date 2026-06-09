#include<bits/stdc++.h>
using namespace std;
string a,b;
int f[1005][1005];
int main(){
	cin>>a>>b;
	int len[3];
	len[1]=a.size();
	len[2]=b.size();
	a=' '+a;
	b=' '+b;
	for(int i=0;i<=len[1];i++){
		f[i][0]=0;
	}
	for(int j=0;j<=len[2];j++){
		f[0][j]=0;
	}
	for(int i=1;i<=len[1];i++){
		for(int j=1;j<=len[2];j++){
			if(a[i]!=b[j]) f[i][j]=max(f[i-1][j],f[i][j-1]);
			else f[i][j]=f[i-1][j-1]+1;
		}
	}
	cout<<f[len[1]][len[2]];
	return 0;
}