#include<bits/stdc++.h>
using namespace std;
int n,m,a[1000005],l,r;
void kp(int l,int r){
	if(l>=r)return;
	int i=l,j=r,x=a[l];
	while(i!=j){
		while(i<j&&a[j]>x)j--;
		if(i<j){a[i]=a[j];i++;}
		while(i<j&&a[i]<=x)i++;
		if(i<j){a[j]=a[i];j--;}
	}
	a[i]=x;
	kp(l,i-1);
	kp(i+1,r);
}
int main(){
	cin>>n;
	for(int i=0;i<n;i++){
		cin>>a[i];
	}
	cin>>m;
	for(int i=1;i<=m;i++){
		cin>>l>>r;
		kp(l-1,r-1);
	}
	for(int i=0;i<n;i++){
		cout<<a[i]<<' ';
	}
	return 0;
}