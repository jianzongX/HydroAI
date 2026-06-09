#include<bits/stdc++.h>
using namespace std;
char a[105];
int cnt[27];
int main(){
	int mx=0,mn=0x3f3f3f3f;
	cin.getline(a,105);
	int len=strlen(a);
	for(int i=0;i<len;i++){
		cnt[a[i]-96]++;
	}
	for(int i=0;i<26;i++){
		mx=max(mx,cnt[i]);
		if(cnt[i]) mn=min(mn,cnt[i]);
	}
	int s=mx-mn;
	bool flag=true;
	if(s==1||s==0) flag=false;
	else{
		for(int i=2;i<=sqrt(s);i++){
			if(s%i==0) {flag=false;break;}
		}
	}
	if(flag==true) printf("Lucky Word\n%d",s);
	else printf("No Answer\n0");
	return 0;
}