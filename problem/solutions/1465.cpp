#include<bits/stdc++.h>
using namespace std;
long long a[100005];
long long n,p=0,ans=0;
int main(){

    cin>>n;
    for(long long i=1;i<=n;i++){
        cin>>a[i];
    }
    for(long long i=1;i<=n;i++){
        if(a[i]>p){
            ans+=a[i]-p;
        }
        p=a[i];
    }
    cout<<ans;
}