#include <bits/stdc++.h>
using namespace std;

vector<int> pre_order;
vector<int> post_order;
vector<vector<int>> children;

//根 -> 子节点
void pre(int node) {
    pre_order.push_back(node);
    for (int child : children[node]) {
        pre(child);
    }
}

//子节点 -> 根
void post(int node) {
    for (int child : children[node]) {
        post(child);
    }
    post_order.push_back(node);
}

int main() {
    int n, m;
    cin >> n >> m;
    children.resize(2001);
    unordered_set<int> x_set, y_set;
    
    for (int i = 0; i < m; ++i) {
        int x, y;
        cin >> x >> y;
        children[x].push_back(y);
        x_set.insert(x);
        y_set.insert(y);
    }
    
    int root = -1;
    for (int x : x_set) {
        if (y_set.find(x) == y_set.end()) {
            root = x;
            break;
        }
    }
    
    pre(root);
    post(root);
    
    for (int i = 0; i < pre_order.size(); ++i) {
        cout << pre_order[i];
        if (i != pre_order.size() - 1) cout << " ";
    }
    cout << endl;
    
    for (int i = 0; i < post_order.size(); ++i) {
        cout << post_order[i];
        if (i != post_order.size() - 1) cout << " ";
    }
    cout << endl;
    
    return 0;
}