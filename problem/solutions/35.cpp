#include<iostream>
#include<cstdio>
#include<cmath>
using namespace std;
int main(){
	int h,r,v;
	cin>>h>>r;
	v=pow(r,2);
	cout<<(int)(20*1000/(h*v*3.14))+1;
	return 0;
}