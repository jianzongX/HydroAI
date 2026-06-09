#include<bits/stdc++.h>
using namespace std;

const int INF = INT_MAX; 
int m, n, n1;                   
vector<pair<int, double>> adj[100005]; 
double dis[100005];               
int cnt[100005] = {0};         
int val[100005] = {0}; 
int x[1005], y[1005];

double distance(double x1, double y1, double x2, double y2) {
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

void spfa(int start, int target) {
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

        for (int i = 0; i < adj[u].size(); i++) {
            int v = adj[u][i].first;
            double w = adj[u][i].second;
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
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> x[i] >> y[i];
    }
    cin >> m;
    for (int i = 0; i < m; i++) {
        int aa, bb;
        cin >> aa >> bb;
        double cc = distance(x[aa], y[aa], x[bb], y[bb]);
        adj[aa].emplace_back(bb, cc);
        adj[bb].emplace_back(aa, cc);
    }
    int s, t;
    cin >> s >> t;
    spfa(s, t);
    printf("%.2f\n", dis[t]);
    return 0;
}