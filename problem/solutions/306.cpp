#include<bits/stdc++.h>
using namespace std;
int main(){
	int a,b,c,Max;
	cin>>a>>b>>c;
	if(a>=b&&a>=c)Max=a;
	if(b>=a&&b>=c)Max=b;
	if(c>a&&c>=b)Max=c;
	cout<<Max<<endl;
	return 0;
}