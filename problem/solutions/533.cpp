#include <bits/stdc++.h>
using namespace std;
int main() {
	int n,a[1001],f[1001]={0},ans=0;
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a[i];
		f[i]=1;
	}
	for(int i=1;i<=n;i++){
		for(int j=1;j<i;j++){
			if(a[i]>a[j])f[i]=max(f[i],f[j]+1);
		} 
	}
	for(int i=1;i<=n;i++){
		ans=max(ans,f[i]);
	}
	cout<<ans;
	return 0;
}