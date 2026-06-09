#include <bits/stdc++.h>
using namespace std;
long long from_dec(long long n, long long p) {
    long long cnt = 0;
    while (n) {
        n /= p;
        cnt += n;
    }
    return cnt;
}

int main() {
    long long n,k;
    cin>>n>>k;
    long long ans=1e18;
    for(long long p=2;p*p<=k;p++){
        if(k%p==0){
            long long ze=0;
            while(k%p==0){
                ze++;
                k/=p;
            }
            long long cnt=from_dec(n,p);
            ans=min(ans,cnt/ze);
        }
    }
    if(k>1){
        long long cnt=from_dec(n,k);
        ans=min(ans,cnt/1);
    }
    cout<<ans;
    return 0;
}