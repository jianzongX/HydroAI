#include<bits/stdc++.h>
using namespace std;
int main(){
	int x,y,z,n;
	cin>>n;
	for(y=1;y<=1000000;y++){
		z=(1+y)*y/2;
		if(z-n>2&&(z-n)%3==0){
			x=(z-n)/3;
			cout<<x<<' '<<y;
			return 0;
		}
	}
	return 0;
}