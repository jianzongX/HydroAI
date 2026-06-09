#include<bits/stdc++.h>
using namespace std;
int n,m;
int a[10005];
int k=1;
int x,y;
int pdX(int N){
	if(N%n==0)return N/n;
	else return N/n+1;
}
int pdY(int K,int X){
	if(X%2==1){
		if(K%n==0)return n;
		else return K%n;
	}
	else {
		if(K%n==0)return 1;
		else return n-(K%n)+1;
	}
}
int main(){
	freopen("seat.in","r",stdin);
	freopen("seat.out","w",stdout);
	cin>>n>>m;
	for(int i=1;i<=n*m;i++){
		cin>>a[i];
	}
	for(int i=2;i<=n*m;i++){
		if(a[i]>a[1]){
			k++;
		}
	}
	x=pdX(k);
	y=pdY(k,x);
	cout<<x<<' '<<y;
	return 0;
}
//2025 CSP-J RP++
//I AK CSP