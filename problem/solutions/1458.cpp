#include <bits/stdc++.h>
using namespace std;
int n,m;
int a[10000005],ans;
int main(){
	cin>>n>>m;
	for(int i=2;i<=m;i++){
		if(a[i]==0){
			for(int j=i;j<=m;j+=i){
				int k=j;
				while(k%i==0){
					a[j]++;
					k/=i;
				}	
			}
		}
	}
	ans=0;
	for(int i=n;i<=m;i++){
		ans=max(ans,a[i]);
	}
	cout<<ans;
	return 0;
}