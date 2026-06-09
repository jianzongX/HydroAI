#include<bits/stdc++.h>
using namespace std;
int a[10000005],n,m,l,r,o,mid;
int main(){
    cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	for(int i=1;i<=m;i++){
		cin>>o;
		l=1;r=n;
        for(int j=1;j<=n;j++){
            mid=(l+r)/2;
			if(a[mid]==o){cout<<"YES"<<endl;break;}
			else if(a[mid]>o)r=mid-1;
			else if(a[mid]<o)l=mid+1;
            if(l>r){cout<<"NO"<<endl;break;}
        }
		}
	return 0;
}