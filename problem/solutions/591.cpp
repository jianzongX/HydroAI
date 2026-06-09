#include<bits/stdc++.h>
using namespace std;
string a,b;
void posorder(int s,int t,int l,int r){
	if(t<s||r<l)return;
	int pos=b.find(a[s]);
	posorder(s+1,s+pos-l,l,pos-1);
	posorder(s+pos-l+1,t,pos+1,r);
	cout<<b[pos];
}
int main(){
	cin>>a>>b;
	posorder(0,a.size()-1,0,b.size()-1);
	return 0;
}