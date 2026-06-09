#include <bits/stdc++.h>
using namespace std;
int b[10005];
int main()
{    
	int l,m,x,y,ans=0;
    cin>>l>>m;for(int i=0;i<=l;i++)b[i]=1;
    for(int i=1;i<=m;i++){
        cin>>x>>y;
        for(int i=x;i<=y;i++)b[i]=0;
    }
    for(int i=0;i<=l;i++)if(b[i]==1)ans=ans+1;
    cout<<ans<<endl;
   
	return 0;
}