#include<bits/stdc++.h>
using namespace std;
string a;
int main() {
    cin>>a;
    int len=a.size();
    for(int i=0;i<len-2;i++){
    	if(a[i]=='#'&&a[i+2]=='#'){
    		cout<<"No";
    		return 0;
		}
	}
    if(len%2==1)cout<<"Yes";
    else cout<<"No";
	return 0;
}