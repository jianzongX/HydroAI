#include<bits/stdc++.h>
using namespace std;
int fa[150005];
int n,k,ans;
int find(int x) {
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}
void merge(int x,int y) {
	int fx=find(x);
	int fy=find(y);
	if(fx!=fy)fa[fy]=fx;
}
int main() {
	cin>>n>>k;
	ans=0;
	for(int i=1; i<=3*n; i++)fa[i]=i;
	for(int i=1; i<=k; i++) {
		int d,x,y;
		cin>>d>>x>>y;
		if(x>n||y>n) {
			ans++;
			continue;
		}
		if(d==1) {
			if(find(x)==find(y+n)||find(x)==find(y+2*n)) {
				ans++;
				continue;
			}
			merge(x,y);
			merge(x+n,y+n);
			merge(x+2*n,y+2*n);
		} else {
			if(x==y) {
				ans++;
				continue;
			}
			if(find(x)==find(y)||find(x)==find(y+2*n)) {
				ans++; 
				continue;
			}
			merge(x,y+n);
			merge(x+n,y+2*n);
			merge(x+2*n,y);
		}
	}
	cout<<ans<<endl;
	return 0;
}