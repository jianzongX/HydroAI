#include<bits/stdc++.h>
using namespace std;
int t,n,f[1000007],b[3000007];
struct node{
    int x,y,e;
}a[1000001];
bool cmp(node a,node b){
    return a.e>b.e;
}
inline void first(int kkk){
    for(int i=1;i<=kkk;i++)
        f[i]=i;
}
int get(int x){
    if(x==f[x]) return x;
    return f[x]=get(f[x]);
}
int main(){
    cin>>t;
    while(t--){
        int tot=-1;
        memset(b,0,sizeof(b));
        memset(a,0,sizeof(a));
        memset(f,0,sizeof(f));
        int flag=1;
        cin>>n;
        for(int i=1;i<=n;i++){
            cin>>a[i].x>>a[i].y>>a[i].e;
            b[++tot]=a[i].x;
            b[++tot]=a[i].y;
        }
        sort(b,b+tot);
        int reu=unique(b,b+tot)-b;
        for(int i=1;i<=n;++i){
            a[i].x=lower_bound(b,b+reu,a[i].x)-b;
            a[i].y=lower_bound(b,b+reu,a[i].y)-b;
        }
        first(reu);
        sort(a+1,a+n+1,cmp);
        for(int i=1;i<=n;i++){
            int r1=get(a[i].x);
            int r2=get(a[i].y);
            if(a[i].e){
                f[r1]=r2;
            }else if(r1==r2){
                cout<<"NO"<<endl;
                flag=0;
                break;
            }
        }
        if(flag)
            cout<<"YES"<<endl;
    }
    return 0;
}