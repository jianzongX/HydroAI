#include<bits/stdc++.h>
using namespace std;
int n,m;
int minn=1000000;
void dfs(int i,int s,int r,int h,int sv) {
	if(s<m-i||s>(m-i)*r*r*h||sv+2*(m-i)>minn)return;

	if(i==m||s==0&&sv<minn) {
		if(i==m&&s==0&&sv<minn)
			minn=sv;
		return;
	}
	for(int j=r-1; j>=m-i; j--) {
		for(int k=h-1; k>=m-i; k--) {
			if(i==0) {
				dfs(i+1,s-j*j*k,j,k,sv+2*j*k+j*j);
			} else dfs(i+1,s-j*j*k,j,k,sv+2*j*k);
		}
	}
	return;
}
int main() {
	cin>>n>>m;
	dfs(0,n,sqrt(n),n,0);
	cout<<minn;
	return 0;
}