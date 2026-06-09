#include <bits/stdc++.h>
using namespace std;
long long n,p;
struct x{
	long long z,a,b;
}y[10005];
long long l=0,r=10e12; 
long long pd(long long x){
	long long t=0;
	for(long long i = 0; i < n; i++){
		if (x <= y[i].z) {
            t += y[i].a * x;
        } else {
            t += y[i].a * y[i].z + y[i].b * (x - y[i].z);
        }
	}
	return t;
}
int main() {
    freopen("power.in", "r", stdin);
    freopen("power.out", "w", stdout);
    cin>>n>>p;
    for(long long i=0;i<n;i++){
    	cin>>y[i].z>>y[i].a>>y[i].b;
	}
	while(l<=r){
		long long mid=l+(r-l)/2;
		if(pd(mid)>=p){
			r=mid-1;
			//cout<<"大于"<<endl; 
		}
		else {
			l=mid+1;
			//cout<<"小于"<<endl;
		}
	}
	cout<<l;
    return 0;
}