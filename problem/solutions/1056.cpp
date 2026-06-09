#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;
    bool flag=true;
    cin>>n;
    for(int i=2;i<=sqrt(n);i++)
    if(n%i==0){
    	flag=false;
    	break;
	}
	if(flag)cout<<"YES";
	else cout<<"NO";
	return 0;
}