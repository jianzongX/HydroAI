#include<bits/stdc++.h>
using namespace std;
int main(){
    long long n,x,max=0,s=1001;
    cin>>n;
    for(int i=1;i<=n;i++){
    	cin>>x;
    	if(x<s)s=x;
    	if(x>max)max=x;
	}
	cout<<max-s;
	return 0;
}