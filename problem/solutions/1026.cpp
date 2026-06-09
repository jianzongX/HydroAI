#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll N=10010,M=105;
inline ll read(){
    ll x=0,f=1;
    char c=getchar();
    while(c<'0'||c>'9'){
        if(c=='-')
          f=-1;
        c=getchar();
    }
    while(c>='0'&&c<='9'){
        x=(x<<1)+(x<<3)+(c^48);
        c=getchar();
    }
    return x*f;
}
inline void write(ll x){
	if(x<0){
		putchar('-');
		x=-x;
	}
	if(x>9)
	  write(x/10);
	putchar(x%10+'0');
}
ll n,m,k;
ll dis[N][M];
bool f[N][M];
vector<pair<ll,ll>> E[N];
priority_queue<pair<ll,ll>,vector<pair<ll,ll>>,greater<pair<ll,ll>>> q;
void add(ll u,ll v,ll w){
	E[u].push_back({v,w});
}
void dijkstra(ll s){
	dis[s][0]=0;
	q.push({0,s});
	while(!q.empty()){
		ll u=q.top().second,p=q.top().first;
		q.pop();
		if(f[u][p%k])
		  continue;
		f[u][p%k]=1;
		for(auto d:E[u]){
			ll v=d.first,w=d.second,t=(p+1)%k;
			if(p>=w)
			  t=p;
			else
			  t=((w-p+k-1)/k)*k+p;
			if(dis[v][(t+1)%k]>t+1){
				dis[v][(t+1)%k]=t+1;
				q.push({t+1,v});
			}
		}
	}
}
int main(){
	memset(dis,0x3f,sizeof(dis));
	n=read(),m=read(),k=read();
	for(int u,v,w,i=0;i<m;i++){
		u=read(),v=read(),w=read();
		add(u,v,w);
	}
	dijkstra(1);
	if(!f[n][0])
	  puts("-1");
	else
	  write(dis[n][0]);
	return 0;
}