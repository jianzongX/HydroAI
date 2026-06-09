#include<bits/stdc++.h>
using namespace std;
long long a,b,n=1;
int main(){
	cin>>a>>b;
	for(int i=1;i<=b;i++){
		n=n*a;
	}
	cout<<n;
	return 0;
}