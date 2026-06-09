#include<bits/stdc++.h>
using namespace std;
int a[100005],b[100005],f[100001],n,ans;
int main(){
    cin>>n;
    for(int i=1;i<=n;i++){
        cin>>a[i]>>b[i];
        f[i]=1;
    }
    for(int i=1;i<=n;i++){
        for(int j=i+1;j<=n;j++){
            if(a[i]>a[j]){
                swap(a[i],a[j]);
                swap(b[i],b[j]);
        }
        }
    }
    for(int i=1;i<=n;i++){
		for(int j=1;j<i;j++){
			if(b[i]>b[j])f[i]=max(f[i],f[j]+1);
		} 
	}
	for(int i=1;i<=n;i++){
		ans=max(ans,f[i]);
	}
	cout<<ans;
	return 0;
}