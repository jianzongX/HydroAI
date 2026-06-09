#include<bits/stdc++.h>
using namespace std;
int s[1000010];
bool vis[1000010];
int main(){
    int n, q, cnt = 0;
    cin >> n;
    for(int i = 2;i <= n;i ++){
        if(!vis[i]) s[++ cnt] = i;
        for(int j = 1;j <= cnt && i * s[j] <= n;j ++){
            if(i * s[j] <= n) vis[i * s[j]] = 1;
            if(i % s[j] == 0) break;
        }
    }
    for(int i=1;i<=cnt;i++){
    	int ans=0;
    	cout<<s[i]<<' ';
		for(int j=1;pow(s[i],j)<=n;j++){
			ans+=n/(pow(s[i],j));
		} 
		cout<<ans<<endl;
	}
    return 0;
}