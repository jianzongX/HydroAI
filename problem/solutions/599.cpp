#include<bits/stdc++.h>
using namespace std;
int fa[100005];
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
	for(int i=1;i<=n*n;i++){
		fa[i]=i;
	}
	for(int i=1;i<=m;i++){
		int x,y;
		char t;
		cin>>x>>y>>t;
		x--;
		y--;
		int curr=x*n+y;
		int ne;
		if(t=='D')ne=(x+1)*n+y;
		else ne=x*n+(y+1);
		if(find(curr)==find(ne)){
			cout<<i<<endl;
			return 0;
		}
		merger(curr,ne);
	}
	cout<<"draw"<<endl;
	return 0;
}