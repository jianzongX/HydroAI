#include<bits/stdc++.h>
using namespace std;
int a[10000005],n,m,l,r,o,mid,b=0;
int main(){
    cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	for(int i=1;i<=m;i++){
		b=0;
		cin>>o;
		l=1;r=n;
        for(int j=1;j<=n;j++){
            mid=(l+r)/2;
			if(a[mid]==o){
                for(int k=1;k<=n;k++){
                if(a[mid+k]!=o){cout<<mid+k-1<<' ';b=1;break;}
            }}
			else if(l>r){cout<<"-1"<<' ';break;}
			else if(a[mid]>o)r=mid-1;
			else if(a[mid]<o)l=mid+1;
		    if(b==1)break;
            
        }
		}
	return 0;
}