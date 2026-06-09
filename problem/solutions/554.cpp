#include<bits/stdc++.h>
using namespace std;
int p[10005];
int dp[5];
int c[5];
int main(){
    int T;
    cin>>T;
    while(T--){
        int n;
        cin>>n;
        for(int i=0;i<n;i++){
        	cin>>p[i];
		}
        dp[0]=dp[1]=dp[2]=0;
        c[1]=c[2]=p[0];
        for(int i=1;i<n;i++){
            c[1]=min(c[1],p[i]-dp[0]);
            dp[1]=max(dp[1],p[i]-c[1]);
            c[2]=min(c[2],p[i]-dp[1]);
            dp[2]=max(dp[2],p[i]-c[2]);
        }
        cout<<dp[2]<<endl;
    }
    return 0;
}