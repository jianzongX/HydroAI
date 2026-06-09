#include<bits/stdc++.h>
using namespace std;
int main() {
	int n,a=0,s=0,b;
	cin>>n;
	for(int i=1; i<=n; i++) {
		if(i%7!=0) {
			b=i;
			while(b!=0) {
				if(b%10==7) {
					a=1;
				}
				b=b/10;
			}
			if(a==0) {
				s=s+i*i;
			}
			a=0;
		}
	}
	cout<<s<<endl;
	return 0;
}