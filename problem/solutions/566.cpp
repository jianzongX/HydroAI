#include<bits/stdc++.h>
using namespace std;
const int fx[10]={0,-2,-1,1,2,2,1,-1,-2};
const int fy[10]={0,1,2,2,1,-1,-2,-2,-1 };
long long f[30][30];
bool vis[30][30];
int main() {
	int bx,by,hx,hy;
	cin>>bx>>by>>hx>>hy;
	bx+=2; 
    by+=2; 
    hx+=2; 
    hy+=2;
	memset(f,0,sizeof(f));
	f[2][1]=1;
	for (int i=0;i<9;i++) {
		int u=hx+fx[i];
		int v=hy+fy[i];
		if (u<0||u>bx||v<0||v>by)
			continue;
		vis[u][v]=true;
	}
	for(int i=2;i<=bx;i++) {
		for(int j=2;j<=by;j++) {
			if (vis[i][j])
				continue;
			f[i][j]=f[i-1][j]+f[i][j-1];
		}
	}
	cout<<f[bx][by];
	return 0;
}