#include<bits/stdc++.h>
using namespace std;
long long n,r,p;
int main(){
    cin>>n>>r>>p;
    long long ping=n/r;
    long long t=ping;
    while(ping>=p){
        long long huan=ping/p;
        t+=huan;
        ping=huan+(ping%p);
    }
    cout<<t;
    return 0;
}