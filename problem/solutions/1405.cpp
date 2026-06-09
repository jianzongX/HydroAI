#include<bits/stdc++.h>
using namespace std;
int n,t,a[100005][5];
map<int,int> vis;
int jdz(int aa) {
	if(aa>=0)return aa;
	else return (0-aa);
}
int main() {
	freopen("dist.in","r",stdin);
	freopen("dist.out","w",stdout);
	cin>>t;
	while(t--) {
		vis.clear();
		cin>>n;
		for(int i=1; i<=n; i++) {
			cin>>a[i][1]>>a[i][2];
			vis[i]=0;
		}
		bool f=0;
		for(int i=1; i<=n; i++) {
			for(int j=i+1; j<=n; j++) {
				if(vis[jdz(a[i][1]-a[j][1])+jdz(a[i][2]-a[j][2])]==0) {
					vis[jdz(a[i][1]-a[j][1])+jdz(a[i][2]-a[j][2])]=1;
				} else {
					f=1;
					break;
				}
				if(f)break;
			}
		}
		if(f==1) {
			cout<<"Yes"<<endl;
		} else {
			cout<<"No"<<endl;
		}
	}
	return 0;
}