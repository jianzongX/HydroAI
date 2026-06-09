#include<bits/stdc++.h>
using namespace std;
int n,a[105],ans[105],minn=1000000;
void dfs(int m){
	if(m>minn)return;
	if(a[m]>n) return;
	if(a[m]==n){
		if(m<minn){
			minn=m;
			for(int i=1;i<=m;i++){
				ans[i]=a[i];
			}
		}
		return;
	}
	for(int i=m;i>=1;i--){
		a[m+1]=a[m]+a[i];
		dfs(m+1);
	}
}
int main(){
	while(cin>>n){
		if(n==0) break;
		a[1]=1;
		minn=1000000;
		dfs(1);
		for(int i=1;i<=minn;i++){
			cout<<ans[i]<<' ';
		}
		cout<<endl;
	}
	return 0;
}