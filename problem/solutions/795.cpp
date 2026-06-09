#include<bits/stdc++.h>
using namespace std;
const int MAXN=1000005;
int n,m;
int r[MAXN];
int d[MAXN],s[MAXN],t[MAXN];
int c[MAXN],b[MAXN];

bool Check(int x)
{
    for(int i=1;i<=n;i++)c[i]=b[i];
    for(int i=1;i<=x;i++)
    {
        c[s[i]]-=d[i];
        c[t[i]+1]+=d[i];
    }
    int sum=0;
    for(int i=1;i<=n;i++)
    {
        sum+=c[i];
        if(sum<0)return 0;
    }
    return 1;
}

int main()
{
    cin>>n>>m;
    for(int i=1;i<=n;i++)
    {
        cin>>r[i];
        b[i]=r[i]-r[i-1];
    }
    for(int i=1;i<=m;i++)
    {
        cin>>d[i]>>s[i]>>t[i];
    }
    int l=1,r=m,ans=0;
    while(l<=r)
    {
        int mid=(l+r)/2;
        if(Check(mid))
        {
            ans=mid;
            l=mid+1;
        }
        else r=mid-1;
    }
    if(ans==m)cout<<0<<endl;
    else cout<<-1<<endl<<ans+1<<endl;
    return 0;
}