#include<bits/stdc++.h>
using namespace std;
string a,m;
long long b[100005];
long long n=1,ans=0;
int main(){
	freopen("number.in","r",stdin);
	freopen("number.out","w",stdout);
    cin>>m>>a;
	long long len=a.size();
	for(long long i=0;i<len;i++){
		if('0'<=a[i]&&a[i]<='9')b[i]=int(a[i]-'0');
		else b[i]=-1;
	}
	b[len]=-1;
	b[len+1]=-1;
	for(long long i=0;i<len-1;i++){
		if(b[i]==-1&&b[i+1]==0){
			if(b[i+2]==-1)continue;
			else b[i+1]=-1;
		}
	}
	for(long long i=len;i+1>=0;i--){
		if(b[i]==-1||i==-1){
			n=1;
			if(b[i+1]!=-1)ans+=5;
			continue;
		}
		else ans+=b[i]*n;
		n*=10;
	}
	cout<<ans;
	return 0;
}