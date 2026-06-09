#include<bits/stdc++.h>
using namespace std;
int n,m,cha,x,y;
int main(){
	freopen("coin.in","r",stdin);
	freopen("coin.out","w",stdout);
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>m;
		if(m%100==0)cha=0;
		else cha=100-m%100;
		x+=cha/10;
		y+=cha%10;
	}
	cout<<x<<' '<<y;
	return 0;
}