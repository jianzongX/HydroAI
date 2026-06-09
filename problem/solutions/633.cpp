#include<bits/stdc++.h>
using namespace std;

const int INF = INT_MAX; 
int n, m;                   
vector<pair<int, int> > adj[100005]; 
int dis[100005];               
int cnt[100005] = {0};         
int val[100005] = {0}; 
int start = 1;

void spfa() {
    for (int i = 1; i <= n; i++) {
        dis[i] = INF;
    }
    dis[start] = 0; 
    
    queue<int> q;
    q.push(start);   
    val[start] = 1;
    cnt[start]++;       
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        val[u] = 0;

        for (vector<pair<int, int> >::iterator it = adj[u].begin(); it != adj[u].end(); ++it) {
            int v = it->first;
            int w = it->second;
            if (dis[v] > dis[u] + w) {
                dis[v] = dis[u] + w;
                if (!val[v]) {
                    q.push(v);
                    val[v] = 1;
                    cnt[v]++;
                    if (cnt[v] > n) {
                        return;
                    }
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
    cout << dis[n] << endl;  
    return 0;
}