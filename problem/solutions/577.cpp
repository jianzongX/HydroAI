#include<bits/stdc++.h>
using namespace std;
int n,a[10005][10005]={0}; 
void jz(int minx,int maxx,int len,int x,int y){
    if(len==1){
        a[x][y]=minx;
        return;
    }
    len=len/2;
    jz(minx,minx+len-1,len,x,y);
    jz(maxx-len+1,maxx,len,x,y+len);
    jz(maxx-len+1,maxx,len,x+len,y);
    jz(minx,minx+len-1,len,x+len,y+len);
}

int main() {
    cin>>n;
    n=pow(2,n);
    jz(1,n,n,1,1); 
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            cout<<a[i][j]<<' ';
        }
        cout<<endl;
    }
    return 0;
}