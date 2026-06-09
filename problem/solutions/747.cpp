#include<bits/stdc++.h>
using namespace std;
long long n,l,r;
int main() {
	freopen("candy.in","r",stdin);
	freopen("candy.out","w",stdout);
	cin>>n>>l>>r;
	if(l/n==r/n) cout<<r%n;
	else cout<<n-1;
	return 0;
}