#include<bits/stdc++.h>
using namespace std;
int main(){
	string a;
	cin>>a;
	int s=a.size();
	if(a.substr(s-2,2)=="er"){
		for(int i=0;i<s-2;i++){
			if(a[i]!=0) cout<<a[i];	
		}
		return 0;
	}
	else if(a.substr(s-2,2)=="ly"){
		for(int i=0;i<s-2;i++){
			if(a[i]!=0) cout<<a[i];	
		}
		return 0;
	}
	else if(a.substr(s-3,3)=="ing"){
		for(int i=0;i<s-3;i++){
			if(a[i]!=0) cout<<a[i];	
		}
		return 0;
	}
	cout<<a;
	return 0;
}