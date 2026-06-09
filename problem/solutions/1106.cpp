#include<bits/stdc++.h>
using namespace std;
int a[105],b[105]={0},n,x,maxx=0;
int main(){
	cin>>n;
	for(int i=0;i<n;i++){
		cin>>a[i];
	}
	for(int i=1;i<n-1;i++){
	    if(a[i-1]<a[i]&&a[i+1]<a[i])b[i]=1;
	}
	for(int i=0;i<n;i++){
		if(b[i]==1){
			x++;
			if(a[i]>maxx){
				maxx=a[i];
			}
		}
	}
	if(x==0)cout<<"No peak!";
	else cout<<x<<" "<<maxx;
	return 0;
}