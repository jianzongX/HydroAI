#include<bits/stdc++.h>
using namespace std;
int main(){
	int s;
	cin>>s;
	if(s/3.0+50>s/1.2)
		cout<<"Walk";
	else if(s/3.0+50<s/1.2)
		cout<<"Bike";
	else
		cout<<"All";
	return 0;
}