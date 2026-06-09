#include<bits/stdc++.h>
using namespace std;
int main(){
    int a=0,b=0,c=0,a1,b1,c1,n;
    cin>>n;
    for(int i=1;i<=n;i++){
    	cin>>a1>>b1>>c1;
    	a=a+a1;
    	b=b+b1;
    	c=c+c1;
	}
	cout<<a<<" "<<b<<" "<<c<<" "<<a+b+c;
	return 0;
}