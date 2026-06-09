#include<bits/stdc++.h>
using namespace std;
int main() {
    int a, b, c;
    cin >> a >> b >> c;
    
    for(int i = 2; i <= a && i <= b && i <= c; i++) 
        if(a % i == b % i && b % i == c % i) {
            cout << i;
            return 0;
        }
}