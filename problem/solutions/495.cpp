#include<bits/stdc++.h>
using namespace std;
const int N=100005;
int a[N],n,m,l,r,mid,ans;
bool ck(int x){
    int s=0,c=1;
    for(int i=1;i<=n;i++){
        if(a[i]>x) return 0;
        if(s+a[i]>x){
            c++;
            s=a[i];
            if(c>m) return 0;
        }else s+=a[i];
    }
    return 1;
}
int main(){
    cin>>n>>m;
    l=0;r=0;
    for(int i=1;i<=n;i++){
        cin>>a[i];
        l=max(l,a[i]);
        r+=a[i];
    }
    while(l<=r){
        mid=(l+r)/2;
        if(ck(mid)){
            ans=mid;
            r=mid-1;
        }else l=mid+1;
    }
    cout<<ans<<endl;
    return 0;
}