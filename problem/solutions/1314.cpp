#include<bits/stdc++.h>
using namespace std;
const int N = 505;
int d[505];
vector<int> g[505];
priority_queue<int, vector<int>, greater<int>> q;
int main(){
    int n, m, cnt = 0;
    cin >> n >> m;
    for(int i = 0; i < m; i++){
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        d[v]++;
    }
    for(int i = 1; i <= n; i++){
        if(d[i] == 0) q.push(i);
    }
    while(!q.empty()){
        int u = q.top();
        q.pop();
        cnt++;
        if(cnt < n) cout << u << ' ';
        else cout << u;
        for(int v : g[u]){
            d[v]--;
            if(d[v] == 0) q.push(v);
        }
    }
    return 0;
}