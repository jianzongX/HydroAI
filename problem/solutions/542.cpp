#include<bits/stdc++.h>
using namespace std;
int a[105],b[105];
int dp[105][1005];
int main()
{
    int t,m;
    cin>>t>>m;
    for(int i=1;i<=m;i++)cin>>a[i]>>b[i];
    for(int i=1;i<=m;i++) 
        for(int j=t;j>=0;j--)  {
            if(j>=a[i])dp[i][j]=max(dp[i-1][j-a[i]]+b[i],dp[i-1][j]);  
            else dp[i][j]=dp[i-1][j];              
        }
    cout<<dp[m][t];
    return 0;
}