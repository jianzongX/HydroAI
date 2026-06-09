#include<bits/stdc++.h>
using namespace std;
const int MOD = 1e9 + 7;
int n;
int main(){
    cin>>n;
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for(int i=2;i*i<=n;i++){
        if(is_prime[i]){
            for(int j=i*i;j<=n;j+=i){
                is_prime[j] = false;
            }
        }
    }//质数 
    long long ans = 1;
    for(int p=2;p<=n;p++){
        if(is_prime[p]){
            long long e = 0;
            long long tmp = n;
            while(tmp){
                tmp /= p;
                e += tmp;
            }
            ans = ans * (2 * e + 1) % MOD;
        }
    }
    cout<<ans<<endl;
    return 0;
}