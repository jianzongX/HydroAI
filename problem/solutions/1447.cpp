#include<bits/stdc++.h>
using namespace std;
long long MOD=1e9+7;

int main() {
	long long n;
	cin>>n;
    vector<long long>a(n+5);
	for(long long i=0;i<n;i++){
		cin>>a[i];
	}
	long long m=a[0];
	for(long long i=1;i<n;i++){
		m=min(m,a[i]);
	}
	long long c=1;
	for(long long i=0;i<n;i++){
		long long ch=a[i]/m;
		c=(c*ch)%MOD;
	}
	cout<<m<<" "<<c;
	return 0;
}