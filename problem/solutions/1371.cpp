#include <iostream>
#include <queue>
#include <vector>
#include <cstring>
using namespace std;

const int MAXK = 10005;
vector<int> adj[MAXK];  
int dis[MAXK];          

int main() {
    int N, K;
    cin >> N >> K;
    for (int i = 0; i < N; ++i) {
        int A, B;
        cin >> A >> B;
        adj[A].push_back(B); 
    }

    memset(dis, -1, sizeof(dis));
    queue<int> q;
    q.push(1); 
    dis[1] = 1;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (u == K) { 
            cout << dis[u] << endl;
            return 0;
        }
        for (int v : adj[u]) {
            if (dis[v] == -1) { 
                dis[v] = dis[u] + 1;
                q.push(v);
            }
        }
    }
    cout << -1 << endl;
    return 0;
}