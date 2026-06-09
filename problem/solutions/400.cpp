#include<bits/stdc++.h>
using namespace std;
int n,a[1005],ans=0;
string b;
int main(){
	cin>>n;
	for(int i=0;i<n;i++){
		cin>>a[i];
		if(ans<a[i]){
			b=" ";
			ans=a[i];
			cin>>b;
		}
	}
	cout<<b;
	return 0;
}