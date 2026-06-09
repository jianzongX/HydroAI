#include<bits/stdc++.h>
using namespace std;
int main() {
	int a[10005];
	int b,c=0,d;
	cin>>b;
	for(int i=1; i<=b; i++) {
		cin>>a[i];
	}
	for(int i=1; i<=b; i++) {
		if(c<a[i]) c=a[i];
	}
	for(int i=0; i<=c; i++) {
		d=0;
		for(int j=1; j<=b; j++) {
			if(a[j]==i) d++;
		}
		cout<<d<<endl;
	}
	return 0;}