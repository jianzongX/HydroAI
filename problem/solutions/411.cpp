#include<bits/stdc++.h>
using namespace std;
int sb(int s){
	if(s==0)return 0;
	return sb(s-1)+s;
}
int main(){
	int n;
	cin>>n;
	cout<<sb(n);
	return 0;
}