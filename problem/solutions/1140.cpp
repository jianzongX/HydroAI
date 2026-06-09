#include<bits/stdc++.h>
using namespace std;
int main(){
	long long x,ans=0;
	cin>>x;
	for(int i=1;i<=x;i++){
		int a;
		cin>>a;
		ans+=a;
	}
	if(ans%2==1){
		cout<<"Alice";
	}
	else{
		cout<<"Bob";
	}
	return 0;
}