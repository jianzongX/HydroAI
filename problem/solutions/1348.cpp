#include <bits/stdc++.h>
using namespace std;

int f1(int num) {
    string s = to_string(num);
    int di[10] = {0};
    for (int i = 0; i < s.length(); i++) {
        int d = s[i] - '0';
        if (d == 0 || di[d]) {
            return 0;
        }
        di[d] = 1;
    }
    return 1;
}

int f2(int num) {
    string s = to_string(num);
    int n = s.size();
    int v[100] = {0}; 
    int c = 0;
    for (int step = 0; step < n; ++step) {
        if (v[c]) {
            return 0;
        }
        v[c] = 1;
        int d = s[c] - '0';
        c = (c + d) % n;
    }
    return c == 0;
}

int main() {
    int m;
    cin >> m;
    int n = m + 1;
    while (1) {
        if (f1(n) && f2(n)) {
            cout << n << endl;
            return 0;
        }
        n++;
    }
}