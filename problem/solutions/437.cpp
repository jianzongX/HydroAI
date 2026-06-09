#include<bits/stdc++.h>
using namespace std;
int a[1005],b[1005],c[1005]={0},d[1005];
int main(){
	int n,m,z=1000000,x;
    cin>>n;
    m=n;
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
    for(int i=0,v=0;i<m;i++){
        if(c[i]==0){
            b[v]=a[i];
            v++;
        };
    }
    for(int j=0;j<n;j++){
        for(int i=0;i<n;i++){
        if(b[i]<z){
        z=b[i];
        x=i;
        }
        }
    d[j]=b[x];
    b[x]=1000000;
    z=1000000;
    }
    int p=0;
    for(int i=0;i<m;i++){
        if(d[i]!=0)p++;
        
    }
    cout<<p<<endl;
    for(int i=0;i<m;i++){
        if(d[i]!=0)cout<<d[i]<<' ';
        
    }
    
	return 0;
}