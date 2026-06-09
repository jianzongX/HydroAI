#include<bits/stdc++.h>
using namespace std;
string a,b;
int f[2005][2005];
int minn(int a,int b,int c){
	return min(a,min(b,c));
}
void dp(string a,string b){
	int len[3];
	len[1]=a.size();
	len[2]=b.size();
	a=' '+a;
	b=' '+b;
	for(int i=0;i<=len[1];i++){
		for(int j=0;j<=len[2];j++){
			f[i][j]=INT_MAX;
		}
	}
	for(int i=0;i<=len[1];i++){
		f[i][0]=i;
	}
	for(int j=0;j<=len[2];j++){
		f[0][j]=j;
	}
	for(int i=1;i<=len[1];i++){
		for(int j=1;j<=len[2];j++){
			if(a[i]!=b[j]){
				f[i][j]=minn(f[i-1][j],f[i][j-1],f[i-1][j-1])+1;
			}
			if(a[i]==b[j])f[i][j]=f[i-1][j-1];
		}
	}
	cout<<f[len[1]][len[2]]<<endl;
}
int main(){
	int n;
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a>>b;
		dp(a,b);
	}
	return 0;
}