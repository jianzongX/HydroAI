#include <bits/stdc++.h>
using namespace std;
int n,a[1001],f[1001][2]={0},ans=0;
void zuo(){
	for(int i=1;i<=n;i++){
		f[i][0]=1;
	}
	for(int i=1;i<=n;i++){
		for(int j=1;j<i;j++){
			if(a[i]>a[j])f[i][0]=max(f[i][0],f[j][0]+1);
		} 
	}
}
void you(){
	for(int i=1;i<=n;i++){
		f[i][1]=1;
	}
	for(int i=n; i>=1; i--) {
        for(int j=i+1; j<=n; j++) {
            if(a[i] > a[j]) {
                f[i][1] = max(f[i][1], f[j][1]+1);
            }
        }
    }
}
int main() {
	cin>>n;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	zuo();
	you();
	int ans=0;
	for(int i=1;i<=n;i++){
		ans=max(ans,f[i][0]+f[i][1]-1);
	}
	cout<<n-ans;
	return 0;
}