#include<bits/stdc++.h>
#define int long long
using namespace std;
int s[1000005];
bool vis[1000005];
int a[1000005];
signed main(){
    int n=1000000,cnt = 0;
    for(int i = 2;i <= n;i ++){
        if(!vis[i]) s[++ cnt] = i;
        for(int j = 1;j <= cnt && i * s[j] <= n;j ++){
            if(i * s[j] <= n) vis[i * s[j]] = 1;
            if(i % s[j] == 0) break;
        }
    }
    int t;
    vis[1]=1;
    while(1){
    	cin>>t;
    	if(t==0)return 0;
    	for(int i=t-1;i>=t/2-1;i--){
    		if(vis[t-i]==0&&vis[i]==0){
    			cout<<t<<" = "<<t-i<<" + "<<i<<endl;
    			break;
			}
		}
	}
    return 0;
}