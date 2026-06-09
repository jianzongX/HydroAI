#include<bits/stdc++.h>
using namespace std;
int n=0,r,c,s=10000;
char a[105][105];
string b;
int main(){
    freopen("encrypt.in","r",stdin);
    freopen("encrypt.out","w",stdout);
    cin>>b;
    n=b.size();
    for(int i=1;i<=sqrt(n);i++){
    	if(n%i==0&&(n/i-i)<s){
		s=(n/i-i);
		r=n/i;
		c=i;
		}
	}
	n=0;
	for(int i=0;i<r;i++){
		for(int j=0;j<c;j++){
			a[j][i]=b[n];
			n++;
		}
	}
	for(int i=0;i<c;i++){
		for(int j=0;j<r;j++){
			cout<<a[i][j];
		}
	}
	return 0;
}
