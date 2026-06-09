#include <bits/stdc++.h>
using namespace std;
string check(string s) {
    bool t0 = 0, t1 = 0;
    for (int i = 0; i < s.size(); ++i) {
        if (s[i] == '0') t0 = 1;
        else t1 = 1;
        if (t0 && t1) break;
    }
    if (t0 && t1) return "F"; 
    if (t0) return "B";       
    return "I";                  
}
string solve(string s) {
    if (s.size() == 1)return check(s);
    int m = s.size() / 2;
    string l = solve(s.substr(0, m));
    string r = solve(s.substr(m));
    string cur = check(s);
    return l + r + cur;
}
int main() {
    int n;
    string s;
    cin >> n >> s;
    int len = 1;
    for (int i = 0; i < n; i++) {
        len *= 2;
    }
    cout << solve(s) << endl;
    return 0;
}