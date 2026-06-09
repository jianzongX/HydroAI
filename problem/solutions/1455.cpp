#include<bits/stdc++.h>
using namespace std;
const int N=100005;
int a,b,p;
vector<int> pri;
bool not_prime[N];
int fa[N];

int find(int x) {
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}

int merger(int x,int y) {
	int fx=find(x);
	int fy=find(y);
	if(fx!=fy)fa[fy]=fx;
	return 0;
}

void pre(int n) {
	for(int i=2;i<=n;i++) {
		if(!not_prime[i])pri.push_back(i);
		for(int pri_j:pri) {
			if(i*pri_j>n)break;
			not_prime[i*pri_j]=true;
			if(i%pri_j==0)break;
		}
	}
}

int main() {
	cin>>a>>b>>p;
	for(int i=a;i<=b;i++)fa[i]=i;
	pre(b);
	
	for(int pri_j:pri) {
		if(pri_j<p)continue;
		int st=-1;
		for(int i=((a+pri_j-1)/pri_j)*pri_j;i<=b;i+=pri_j) {
			if(st==-1)st=i;
			else merger(st,i);
		}
	}
	
	int ans=0;
	for(int i=a;i<=b;i++) {
		if(find(i)==i)ans++;
	}
	cout<<ans<<endl;
	return 0;
}