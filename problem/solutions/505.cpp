#include<bits/stdc++.h>
using namespace std;
int n,k,vis[200005]={0};
struct node{
	int x,y;
};
int bfs(int sn,int st){
	queue<node>q;
	q.push({sn,st});
	vis[sn]=1;
	while(!q.empty()){
		
		node f=q.front();vis[f.x]=1;if(f.x==k)return f.y;
		q.pop();
	
		if(f.x+1<200000&&vis[f.x+1]==0){q.push({f.x+1,f.y+1});
		}
		if(f.x-1>0&&vis[f.x-1]==0){q.push({f.x-1,f.y+1});
		}
		if(f.x*2<200000&&vis[f.x*2]==0){q.push({f.x*2,f.y+1});
		}
	}
	return 0;
}
int main() {
	cin>>n>>k;
	cout<<bfs(n,0);
	return 0;
}