#include<bits/stdc++.h>
using namespace std;
int fa[100005];
int faN[100005];
int n,m;
int find(int x){
	if(x==fa[x])return x;
	fa[x]=find(fa[x]);
	return fa[x];
}
int merger(int x,int y){
	int fx = find(x);
    int fy = find(y);
    if (fx == fy) {
        return 0;
    }
    faN[fx] += faN[fy];
    fa[fy] = fx;
    return 0;
}

int main(){
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		fa[i]=i;
		faN[i]=1;
	}
	for(int i=1;i<=m;i++){
		char a;
		int pa,pb;
		cin>>a;
		if(a=='M'){
			cin>>pa>>pb;
			merger(pa,pb);
		}
		else{
			cin>>pa;
			cout<<faN[find(pa)]<<endl;
		}
	}
	return 0;
}