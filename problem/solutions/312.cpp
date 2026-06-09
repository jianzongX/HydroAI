#include<bits/stdc++.h>
using namespace std;
int main(){
    int ans=0,x,n;
    double ave;
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
    	scanf("%d",&x);
    	ans=ans+x;
	}
	ave=ans*1.0/n;
	printf("%.2lf",ave);
	return 0;
}