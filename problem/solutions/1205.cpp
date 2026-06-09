#include <bits/stdc++.h>
using namespace std;
vector<int> g[1005];
int vis[1005];
int main() {
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
    }
    for (int i = n; i >= 1; i--) {
        vis[i] = i; 
        for (int j = 0; j < g[i].size(); j++) {
        	int v = g[i][j];
            vis[i] = max(vis[i], vis[v]);
            vis[i] = max(vis[i], vis[v]);
        }
    }
    for (int i = 1; i <= n; i++) {
        cout << vis[i] << " ";
    }
    cout << endl;
    return 0;
}