#include<bits/stdc++.h>
using namespace std;

const int INF = INT_MAX; 
int n, m;                   
vector<pair<int, int> > adj[105]; 
int dis[105];               
int val[105] = {0}; 
int start = 1;

void spfa() {
    for (int i = 1; i <= n; i++) {
        dis[i] = INF;
    }
    dis[start] = 0; 
    
    queue<int> q;
    q.push(start);   
    val[start] = 1;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        val[u] = 0;
        for (vector<pair<int, int>>::iterator it = adj[u].begin(); it != adj[u].end(); it++) {
            int v = it->first;
            int w = it->second;
            if (dis[v] > dis[u] + w) {
                dis[v] = dis[u] + w;
                if (!val[v]) {
                    q.push(v);
                    val[v] = 1;
                }
            }
        }
    }
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int aa, bb, cc;
        cin >> aa >> bb >> cc;
        adj[aa].emplace_back(bb, cc);
        adj[bb].emplace_back(aa, cc);
    }
    
    spfa();
    int max_time = 0;
    for (int i = 1; i <= n; i++) {
        if (dis[i] == INF) {
            cout << -1 << endl; 
            return 0;
        }
        max_time = max(max_time, dis[i]);
    }
    
    cout << max_time << endl;  
    return 0;
}