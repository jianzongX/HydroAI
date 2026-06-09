#include<bits/stdc++.h>
using namespace std;
int n,a[1000005];
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
	kp(0,n-1);
	for(int i=0;i<n;i++){
		cout<<a[i]<<' ';
	}
	return 0;
}