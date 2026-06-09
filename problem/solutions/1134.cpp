#include<bits/stdc++.h>
using namespace std;
#define ll long long
int a,b,p;
ll f(ll a, ll b, ll q){
    if(b == 0) return 1;
    if(b == 1) return a % q;
    ll x = f(a, b / 2, q);
    if(b % 2 == 0) return (x * x) % q;
    else return (((x * x) % q) * a) % q;
}
int main(){
	cin>>a>>b>>p;
	cout<<f(a,b,p);
}