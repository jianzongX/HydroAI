#include<bits/stdc++.h>
using namespace std;
int a[40005];
int main(){
	int n,m,o=0,k=1;cin>>n;
	while(cin>>m){
		for(int i=1;i<=m;i++){
			cout<<o;
			if(k%n==0)cout<<endl;
			k++;
		}
		if(o==0)o=1;
		else o=0;
	}
	return 0;
}