#include<bits/stdc++.h>
using namespace std;
int s[1001];
int num(int n){
	if(s[n]!=0)return s[n];
	int sum=1;
	for(int i=n/2;i>0;i--){
		sum+=num(i);
	}
	s[n]=sum;
	return s[n];
}
int main(){
	int n;
	cin>>n;
	cout<<num(n);
	return 0;
}