#include<bits/stdc++.h>
using namespace std;

const int maxx = 100005;
const double INF = 1e18;
int n, m;
vector<pair<int, double>> adj[maxx];
double dis[maxx];
bool vis[maxx];

void dijkstra(int t) {
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> pq;
    for (int i = 1; i <= n; i++) {
        dis[i] = INF;
        vis[i] = false;
    }
    dis[t] = 100.0;
    pq.push({dis[t], t});
    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        if (vis[u]) continue;
        vis[u] = true;
        for (auto &edge : adj[u]) {
            int v = edge.first;
            double rate = 1.0 - edge.second / 100.0;
            if (dis[v] > dis[u] / rate) {
                dis[v] = dis[u] / rate;
                pq.push({dis[v], v});
            }
        }
    }
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int x, y, z;
        cin >> x >> y >> z;
        adj[x].emplace_back(y, z);
        adj[y].emplace_back(x, z);
    }
    int A, B;
    cin >> A >> B;
    dijkstra(B);
    printf("%.8f\n", dis[A]);
    return 0;
}