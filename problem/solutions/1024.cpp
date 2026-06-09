#include<bits/stdc++.h>
using namespace std;
long long n,d,v[100005],a[100005];
long long mini=0x3f3f3f3f;
long long N=0,M=0;
int main(){
	freopen("road.in","r",stdin);
	freopen("road.out","w",stdout);
    cin>>n>>d;
    for(long long i=1;i<n;i++){
    	cin>>v[i];
	}
	for(long long i=1;i<=n;i++){
		cin>>a[i];
	}
	mini=a[1];
	for(long long i=1;i<n;i++){
		mini=min(a[i],mini);
		if(N<v[i]){
			long long need=(v[i]-N + d - 1)/d;
			M+=need*mini;
			N+=need*d;
		}
		N-=v[i];
	}
	cout<<M;
	return 0;
}