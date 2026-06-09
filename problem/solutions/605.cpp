#include<bits/stdc++.h>
using namespace std;
char a[260];
int x=0,y=0; 
int main(){
	cin>>a;
	int i=0;
	while(a[i]!='@'){
		if(a[i]=='(')x++;
		if(a[i]==')')y++;
        i++;
	}
	if(x==y)cout<<"YES";
	else cout<<"NO";
	return 0;
}