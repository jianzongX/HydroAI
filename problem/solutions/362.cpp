#include <bits/stdc++.h>
using namespace std;
int n,a[105];
int main()
{
    int n,m,b=0;cin>>n>>m;
    for(int i=1;i<=n;i++)a[i]=1;
    for(int i=1;i<=m;i++){
        for(int j=i;j<=n;j+=i){
            if(a[j]==1)a[j]=0;
            else a[j]=1;
        }
    }
    for(int i=1;i<=n;i++)if(a[i]==0){
        if(b==0){cout<<i;
        b+=1;}
        else cout<<","<<i;
    }
	return 0;
}