#include<bits/stdc++.h>
using namespace std;
int main(){
	double a,b=0;
	cin>>a;
	for(int i=1;i<=10;i++){
		b = a+b;
		a = a*0.5;
		b = a+b;
	}
	cout<<b-a<<endl<<a;
	return 0;
}