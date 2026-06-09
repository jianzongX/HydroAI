#include <bits/stdc++.h>
using namespace std;
int n,m,f[10001]={0},c[10001]={0};
int x,y,root,maxx=0,maxi=1;
int main()
{
	cin>>n>>m;
	for(int i=1;i<=m;i++){
		cin>>x>>y;
		f[y]=x; 
	}
	for (int i=1;i<=n; i++) {
        if (f[i] == 0) {
            root = i;
            break;
        }
    }
	for(int i=1;i<=n;i++){
		c[f[i]]++;
	}
	for(int i=1;i<=n;i++){
		if(maxx<c[i]){
			maxx=c[i];
			maxi=i;
		}
	}
	cout<<root<<endl<<maxi<<endl;
	for(int i=1;i<=n;i++){
		if(f[i]==maxi){
			cout<<i<<" ";
		}	
	}
	return 0;
}