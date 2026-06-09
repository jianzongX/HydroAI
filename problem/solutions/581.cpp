#include<bits/stdc++.h>
using namespace std;
char a[105][105];
int n,m,ans=0,vis[105][105],d[4][2]={{0,-1},{0,1},{-1,0},{1,0}};
struct node{
	int x,y;
};
void bfs(int si,int sj){
	queue<node>q;
	q.push({si,sj});
	vis[si][sj]=1;
	while(!q.empty()){
		node f=q.front();
		q.pop();
		for(int i=0;i<4;i++){
			int sx=f.x+d[i][0],sy=f.y+d[i][1];
			if(sx<1||sx>n||sy<1||sy>m||vis[sx][sy]==1||a[sx][sy]=='0')continue;
			q.push({sx,sy});
			vis[sx][sy]=1;
		}
	}
}
int main() {
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			cin>>a[i][j];
		}
	}
	for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			if(a[i][j]!='0'&&vis[i][j]==0){
				bfs(i,j);
				ans++;
			}
		}
	}
	cout<<ans;
	return 0;
}