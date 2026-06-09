#include<bits/stdc++.h>
#define int long long
using namespace std;
int s[100000010];
bool vis[100000010];
signed main(){
    int n, q, cnt = 0;
    scanf("%lld%lld", &n, &q);
    //cin >> n >> q;
    for(int i = 2;i <= n;i ++){
        if(!vis[i]) s[++ cnt] = i;
        for(int j = 1;j <= cnt && i * s[j] <= n;j ++){
            if(i * s[j] <= n) vis[i * s[j]] = 1;
            if(i % s[j] == 0) break;
        }
    }

    while(q --){
        int t;
        scanf("%lld", &t);
        //cin >> t;
        //cout << s[t] << '\n';
        printf("%lld\n", s[t]);
    }

    return 0;
}