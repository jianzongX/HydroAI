#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    priority_queue<int, vector<int>, less<int>> q2;  
    priority_queue<int, vector<int>, greater<int>> q1;

    for (int i = 0; i < n; ++i) {
        cin >> a[i];

        if (q2.empty() || a[i] <= q2.top()) {
            q2.push(a[i]);
        } else {
            q1.push(a[i]);
        }
        while (q2.size() > q1.size() + 1) {
            q1.push(q2.top());
            q2.pop();
        }
        while (q1.size() > q2.size()) {
            q2.push(q1.top());
            q1.pop();
        }
        if ((i + 1) % 2 == 1) {
            cout << q2.top() << endl;
        }
    }

    return 0;
}