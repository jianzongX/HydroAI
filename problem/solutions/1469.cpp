#include<bits/stdc++.h>
using namespace std;
int n,m;
int a[1000005];
int p[1000005];
long long d1[1000005];
long long d2[1000005];
bool check(int k) {
	memset(d1,0,sizeof(d1));
	memset(d2,0,sizeof(d2));
	for(int i=1; i<=m; ++i) {
		int x=p[i];
		int l=x-k+1;
		int r=x+k-1;
		int L=max(l,1);
		int R=min(x,r);
		d1[L]++;
		d1[R+1]--;
		d2[L]+=k-x;
		d2[R+1]-=k-x;
		L=max(x+1,l);
		R=min(r,n);
		d1[L]--;
		d1[R+1]++;
		d2[L]+=k+x;
		d2[R+1]-=k+x;
	}
	long long c1=0,c2=0;
	for(int i=1; i<=n; ++i) {
		c1+=d1[i];
		c2+=d2[i];
		long long res=c1*i+c2;
		if(res<a[i])return 0;
	}
	return 1;
}
int main() {
	cin>>n>>m;
	for(int i=1; i<=n; ++i)cin>>a[i];
	for(int i=1; i<=m; ++i)cin>>p[i];
	int l=1,r=1e9,ans=r;
	while(l<=r) {
		int mid=l+(r-l)/2;
		if(check(mid)) {
			ans=mid;
			r=mid-1;
		} else l=mid+1;
	}
	cout<<ans<<endl;
	return 0;
}