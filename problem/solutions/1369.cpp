#include <bits/stdc++.h>
using namespace std;
const long long INF = 0x3f3f3f3f3f3f3f3f;

struct Edge {
    long long to, val;
};

long long n, m;
vector<Edge> adj[100005]; 
long long dis[100005]; 

void Dijkstra(long long s) {
    fill(dis, dis + n + 1, INF);
    dis[s] = 0;
    priority_queue<pair<long long, long long>, vector<pair<long long, long long>>, greater<pair<long long, long long>>> pq;
    pq.push({0, s});
    
    while (!pq.empty()) {
        auto [dist_u, u] = pq.top();
        pq.pop();
        if (dist_u > dis[u]) continue;
        
        for (const Edge& e : adj[u]) {
            long long v = e.to, val = e.val;
            if (dis[v] > dis[u] + val) {
                dis[v] = dis[u] + val;
                pq.push({dis[v], v});
            }
        }
    }
}

int main() {
    cin >> n >> m;
    
    for (long long i = 0; i < m; i++) {
        long long a, b, c;
        cin >> a >> b >> c;
        adj[a].push_back({b, c});
        adj[b].push_back({a, c});
    }
    
    if (n == 1) {
        cout << 0 << endl;
        return 0;
    }
    
    Dijkstra(1);
    
    if (dis[n] >= INF / 2) {
        cout << -1 << endl;
    } else {
        cout << dis[n] << endl;
    }
    
    return 0;
}