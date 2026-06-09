#include<bits/stdc++.h>
using namespace std;
string s;
long long a[1000005];
long long n=0;
bool cmp(long long a,long long b){
	return a>b;
}
int main(){
	freopen("number.in","r",stdin);
	freopen("number.out","w",stdout);
	cin>>s;
	for(long long i=0;i<s.size();i++){
		if(s[i]>='0'&&s[i]<='9'){
			a[n]=s[i]-'0';
			n++;
		}
	}
	sort(a,a+n,cmp);
	for(long long i=0;i<n;i++){
		cout<<a[i];
	}
	return 0;
}
//2025 CSP-J RP++
//I AK CSP