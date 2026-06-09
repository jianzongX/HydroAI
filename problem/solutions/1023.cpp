#include<bits/stdc++.h>
using namespace std;
long long n,m=0,sum=0,ans=0;
int a=0;
int main(){
	cin>>n;
	while(n!=0){
		m=0;
		sum++;
		if(a==0 && n%3==1){
			a=1;
			ans=sum;
		}
		if(n%3!=0){
			m=n/3;
			m+=1;
			n-=m;
		}
		else if(n%3==0){
			m=n/3;
			n-=m;
		}
	}
	cout<<sum<<" "<<ans<<'\n';
	return 0;
}