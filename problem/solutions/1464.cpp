#include<bits/stdc++.h>
using namespace std;
int a[1000005];
int mb;
int main(){
    int n;
    cin>>n;
    while(n--){
        int a1,b1;
        cin>>a1>>b1;
        mb=max(mb,b1);
        a[a1]++;
        a[b1+1]--;
    }
    int ans=0,maxx=0;
    for(int i=0;i<=mb;i++){
        ans+=a[i];
        maxx=max(maxx,ans);
    }
    cout<<maxx;
    return 0;
}