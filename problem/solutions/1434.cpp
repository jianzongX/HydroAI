#include<bits/stdc++.h>
using namespace std;
int fa[500005],dis[500005],sz[500005];
int t;

int find(int x){
    if(x==fa[x]) return x;
    int fx=find(fa[x]);
    dis[x]+=dis[fa[x]];
    fa[x]=fx;
    return fx;
}

void merge(int x,int y){
    int fx=find(x),fy=find(y);
    if(fx==fy) return;
    fa[fx]=fy;
    dis[fx]=sz[fy];
    sz[fy]+=sz[fx];
}

int main() {
	cin>>t;
    for(int i=1;i<=t;i++){
        fa[i]=i;
        dis[i]=0;
        sz[i]=1;
    }
    while(t--){
        char a;
        int b,c;
        cin>>a>>b>>c;
        if(a=='M'){
            merge(b,c);
        }else{
            if(b == c){
                cout<<0<<endl;
                continue;
            }
            int fx=find(b),fy=find(c);
            if(fx!=fy){
                cout<<-1<<endl;
            }else{
                cout<<abs(dis[b]-dis[c])-1<<endl;
            }
        }
    }
    return 0;
}