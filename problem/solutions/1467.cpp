#include<bits/stdc++.h>
using namespace std;
int n,m,a[5005];
int b[5005];
int tmp[5005];
int ansK, ansM = 1e9;
int main(){
    cin>>n;
    for(int i=1;i<=n;i++){
        string t;
        cin>>t;
        if(t=="B")a[i]=1;
        else a[i]=0;
    }
    for(int i=1;i<=n;i++){
        b[i]=a[i]^a[i-1];
    }
    for(int k=1;k<=n;k++){
        memcpy(tmp, b, sizeof(b));
        int cnt=0;
        bool ok = true;
        for(int i=1;i<=n;i++){
            if(tmp[i]==1){
                if(i + k - 1 > n){
                    ok = false;
                    break;
                }
                cnt++;
                tmp[i] ^= 1;
                if(i + k <= n) tmp[i + k] ^= 1;
            }
        }
        if(ok && cnt < ansM){ 
            ansM = cnt;
            ansK = k;
        }

    }
    cout << ansK << " " << ansM << endl;
    return 0;
}