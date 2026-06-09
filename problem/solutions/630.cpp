#include<bits/stdc++.h>
using namespace std;

const long long INF = LLONG_MAX; 
long long n, v0;                   
long long a[1005][1005];         
long long dis[10005];               
long long cnt[10005] = {0};         
long long vv[10005] = {0}; 

void spfa() {
    for (long long i = 1; i <= n; i++) {
        dis[i] = INF;
    }
    dis[v0] = 0; 
    
    queue<int> q;
    q.push(v0);   
    vv[v0] = 1;
    cnt[v0]++;       
    
    while (!q.empty()) {
        long long u = q.front();
        q.pop();
        vv[u] = 0;

        for (long long v = 1; v <= n; v++) {
            if (a[u][v] != INF) {
                
                if (dis[v] > dis[u] + a[u][v]) {
                    dis[v] = dis[u] + a[u][v];
                    if (!vv[v]) {
                        q.push(v);
                        vv[v] = 1;
                        cnt[v]++;
                        if (cnt[v] > n) {
                            return;
                        }
                    }
                }
            }
        }
    }
}

int main() {
    cin >> n;
    cin >> v0;
    for (long long i = 1; i <= n; i++) {
        for (long long j = 1; j <= n; j++) {
            a[i][j] = INF; 
        }
    }

    for (long long i = 1; i <= n; i++) {
        for (long long j = 1; j <= n; j++) {
            string val;
            cin >> val;
            if (val == "-") {
                a[i][j] = INF; 
            } else {
                a[i][j] = stol(val); 
            }
        }
    }
    spfa();
    for (long long i = 1; i <= n; i++) {
        if (i == v0) continue;
        cout << "(" << v0 << " -> " << i << ") = " << dis[i] << endl;
    }
    
    return 0;
}