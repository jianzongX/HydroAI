#include<bits/stdc++.h>
using namespace std;
deque<int> q;
int a[1005] = {0};
int n, m, num = 0, t;
int main() {
    cin >> n >> m;
    for(int i = 0; i < m; i++) {
        cin >> t;
        if(a[t]) continue;
        num++;
        if(q.size() < n) {
            q.push_back(t);
            a[t] = 1;
        } else {
            int x = q.front();
            q.pop_front();
            a[x] = 0;
            q.push_back(t);
            a[t] = 1;
        }
    }
    cout << num;
    return 0;
}