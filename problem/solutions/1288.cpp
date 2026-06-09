#include <bits/stdc++.h>
using namespace std;
int main() {
	set <string> S;
	int n;cin >> n;
	for (int i=1;i<=n;i++) {
		string s;
		cin >> s;
		S.insert(s);
	}
	cout << 52-S.size() << endl;
	return 0;
}