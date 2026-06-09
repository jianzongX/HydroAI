# include <bits/stdc++.h>
using namespace std;
int main(){
	int a,b,c;
	cin>>a>>b>>c;
	if (c<a+b && a<b+c && b<a+c)
		cout<<"yes";
	else
		cout<<"no";

	return 0;
}