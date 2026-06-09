#include<bits/stdc++.h>
using namespace std;
int main(){
	long long int a,b,c,d;
	cin>>a>>b;
	c=a;
	d=a;
	for(int i=1;i<b;i++)
	{
	a=d;
	a=c*a;
	c=a%7;
	}
	if(c==1)
	cout<<"Monday";
	if(c==2)
	cout<<"Tuesday";
	if(c==3)
	cout<<"Wednesday";
	if(c==4)
	cout<<"Thursday";
	if(c==5)
	cout<<"Friday";
	if(c==6)
	cout<<"Saturday";
	if(c==0)
	cout<<"Sunday";
		return 0;
}