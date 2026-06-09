#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll n,m,s,y,ans;
ll w[200010],v[200010],l[200010],r[200010],q1[200010],q2[200010];
bool check(ll wq){
	y=0;
	memset(q1,0,sizeof(q1));
	memset(q2,0,sizeof(q2));
	for(int i=1;i<=n;i++){
		if(w[i]>wq)q1[i]=q1[i-1]+1,q2[i]=q2[i-1]+v[i];
		else q1[i]=q1[i-1],q2[i]=q2[i-1];
	}
	for(int i=1;i<=m;i++){
		int L=l[i],R=r[i];
		y+=(q1[R]-q1[L-1])*(q2[R]-q2[L-1]);
	}
	return y>s;
}
int main(){
	cin>>n>>m>>s;
	for(int i=1;i<=n;i++)cin>>w[i]>>v[i];
	for(int i=1;i<=m;i++)cin>>l[i]>>r[i];
	ll L=1,R=2000010;
	ans=s;
	while(L<=R){
		ll mid=L+(R-L)/2;
		if(check(mid))L=mid+1;
		else R=mid-1;
		ans=min(ans,llabs(s-y));
	}
	cout<<ans;
	return 0;
}