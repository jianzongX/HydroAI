#include<bits/stdc++.h>
using namespace std;
int n,r,a[55];
void f(int k,int i){
	if(k==r+1){
        for(int i=1;i<=r;i++)cout<<a[i]<<' ';
        cout<<endl;
        return;
    }
    for(int j=i+1;j<=n;j++){
	    a[k]=j;
        f(k+1,j);
    }
}
int main(){
	cin>>n>>r;
    f(1,0);
	return 0;
}