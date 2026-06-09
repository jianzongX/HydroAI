#include <bits/stdc++.h>
using namespace std;
long long c(const vector<long long>& cables, long long len) {
    long long cnt = 0;
    for (long long c : cables) {
        cnt += c / len;
    }
    return cnt;
}
int main(){
    int N, K;
    cin >> N >> K;
    vector<long long> cables(N);
    long long total = 0;
    for (int i = 0; i < N; ++i) {
        double len;
        cin >> len;
        cables[i] = (round(len * 100));
        total += cables[i];
    }
    if(total<K){
        cout<<"0.00"<<endl;
        return 0;
    }
    long long l=1;
    long long r=total/K;
    long long ans = 0;
    while (l <= r) {
        long long mid = l + (r - l) / 2; 
        long long cnt = c(cables, mid);
        if (cnt >= K) {
            ans = mid; 
            l = mid + 1; 
        } else {
            r = mid - 1; 
        }
    }

    cout<<fixed<<setprecision(2) << (ans / 100.0) << endl;
    return 0;
}