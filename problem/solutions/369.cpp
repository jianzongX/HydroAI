#include<bits/stdc++.h>
using namespace std;
int main(){
	int a[100000];
	int n,c=0,b,x=0;
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	for(int i=1;i<=n;i++){
		if(c<a[i]){
			c=a[i];
		} 
	}
	for(int i=0;i<=c;i++){
		b = 0;
		for(int j=1;j<=n;j++){
			if(a[j]==i){
				b++;	
			} 
		}
		if(b>x){
			x=b;
		}
	}
	cout<<x;
	return 0;
}