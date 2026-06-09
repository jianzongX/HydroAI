#include<bits/stdc++.h>
using namespace std;
int main(){
    int k,a=1,b=1,c;
    cin>>k;
    for(int i=1;i<=k-2;i++){
    	c=a+b;
    	a=b;
    	b=c;
	}
	cout<<c;
	return 0;
}