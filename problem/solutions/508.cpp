#include<bits/stdc++.h>
using namespace std;
char a[205][205];
int ci,cj,nm,n,m,vis[205][205],d[4][2]= {{0,-1},{0,1},{-1,0},{1,0}};
void cs() {
	for(int i=0; i<=205; i++) {
		for(int j=0; j<=205; j++) {
			vis[i][j]=0;
		}
	}
}
struct node {
	int x,y,t;
};
void bfs(int si,int sj,int st) {
	vis[si][sj]=1;
	queue<node>q;
	q.push({si,sj,st});
	vis[si][sj]=1;
	while(!q.empty()) {
		node f=q.front();
		if(a[f.x][f.y]=='E'){cout<<f.t<<endl;return;
		}
		q.pop();
		for(int i=0; i<4; i++) {
			int sx=f.x+d[i][0],sy=f.y+d[i][1];
			if(sx<1||sx>n||sy<1||sy>m||vis[sx][sy]==1||a[sx][sy]=='#')continue;
			q.push({sx,sy,f.t+1});
			vis[sx][sy]=1;
		}
	}
	cout<<"oop!"<<endl;
	return;
}
int main() {
	cin>>nm;
	while(nm--){
		cin>>n>>m;
		for(int i=1; i<=n; i++) {
			for(int j=1; j<=m; j++) {
				cin>>a[i][j];
				if(a[i][j]=='S'){
					ci=i;
					cj=j;
				}
			}
		}
		bfs(ci,cj,0);
		cs();
	}
	return 0;
}