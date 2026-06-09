#include<bits/stdc++.h>
using namespace std;
int x,y;
int gcd(int a,int b){
    while(b){
        a%=b;
        swap(a,b);
    }
    return a;
}
int main(){
    cin>>x>>y;
    if(y%x!=0){
        cout<<0;
        return 0;
    }
    int n=y/x;
    int cnt=0;
    for(int i=1;i*i<=n;i++){
        if(n%i==0){
            int j=n/i;
            if(gcd(i,j)==1){
                cnt+=2;
            }
        }
    }
    cout<<cnt;
    return 0;
}