#include<bits/stdc++.h>
using namespace std;
int main() {
	int m;
	cin>>m;
	while(m--){
		int n;
		cin>>n;
		int cnt=0;
		for(int i=2; i*i<=n; i++) {
			if(n%i==0){
				cnt++;
				while(n%i==0){
					n/=i;
				}
			}
		}
		if(n>1){
			cnt++;
		}
		if(cnt==2)cout<<1<<endl;
		else cout<<0<<endl;
	} 
	return 0;
}