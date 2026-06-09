#include<bits/stdc++.h>
using namespace std;
int n,d[1000005];
int td=1;
int ans;
int main(){
    cin>>n;
    for(int i=1;i<=n;i++){
        cin>>d[i];
    }
    while(td<=n){
        if(d[td]==0){
            td++;
            continue;
        }
        for(int i=td;d[i]!=0;i++){
            d[i]--;
        }
        ans++;
    }
    cout<<ans;
    return 0;
}