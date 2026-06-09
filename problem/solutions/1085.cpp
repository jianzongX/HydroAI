#include<bits/stdc++.h>
using namespace std;
int a[1000005],n,m,q,l,r,mid;
int main(){
    cin>>n>>m;
    for(int i=1;i<=n;i++){
        cin>>a[i];
    }
    for(int i=1;i<=m;i++){
        cin>>q;
        l=1; r=n;
        int ans=-1;
        while(l<=r){
            mid=(l+r)/2;
            if(a[mid]>=q){
                if(a[mid]==q) ans=mid;
                r=mid-1;
            }
            else l=mid+1;
        }
        cout<<ans<<' ';
    }
    return 0;
}