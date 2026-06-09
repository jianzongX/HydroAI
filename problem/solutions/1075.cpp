#include<bits/stdc++.h>
using namespace std;
int main(){
	long long n,x,max=0,s=0;
    cin>>n;
    for(int i=1;i<=n;i++){
    	cin>>x;
    	if(x>max){max=x;s=i;
	}
	}
	cout<<max<<" "<<s;
	return 0;
}