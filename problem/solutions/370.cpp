#include<bits/stdc++.h>
using namespace std;
int a[20005],c[20005]={0};
int main(){
	int n;
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    for(int i=0;i<n;i++){
        for(int j=1;j<=n;j++){
            if(i==j)break;
            if(a[i]==a[j]){
                if(i>j)c[i]=1;
                else c[j]=1;
            }
            }
        }
    
    for(int i=0;i<n;i++){
        if(c[i]==0)cout<<a[i]<<' ';
    }
    
	return 0;
}