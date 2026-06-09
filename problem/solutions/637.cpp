#include<bits/stdc++.h>
using namespace std;
int fa[100005];
int a[100005];
int n,m;
int find(int x){
	if(x==fa[x])return x;
	fa[x]=find(fa[x]);
	return fa[x];
}
int merger(int x,int y){
	int fx = find(x);
    int fy = find(y);
    fa[fy] = fx;
    return 0;
}
int main(){
	cin>>n>>m;
	for(int i=1;i<=2*n;i++){
		fa[i]=i;
	}
	for(int i=1;i<=m;i++){
		int p,x,y;
		cin>>p>>x>>y;
		if(p==0){
			merger(x,y);	
		}
		if(p==1){
			merger(x,y+n);
			merger(x+n,y);		
		}
	}
	for(int i=1;i<=n;i++){
		a[find(i)]=1;
	}
	int b=0;
	for(int i=1;i<=2*n;i++){
		if(a[i]==1)b++;
	}
	cout<<b;
	return 0;
}