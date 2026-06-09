#include <bits/stdc++.h>
using namespace std;
int a[20000];
int f[20000];
int main() {
	int n,t;
	cin>>n>>t;
	for(int i=1; i<=n; i++) {
		cin>>a[i];
	}
	f[0]=1;
	for(int i=1; i<=n; i++) {
		for(int j=t; j>=a[i]; j--) {
			f[j]=f[j]+f[j-a[i]];
		}
	}
	cout<<f[t];
	return 0;
}