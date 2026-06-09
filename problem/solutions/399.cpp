#include<bits/stdc++.h>
using namespace std;
string a,c;
int main(){
    cin>>a;
    c=a;
    int b=a.size();
    for(int i=0;i<b;i++){  
        c[b-i-1]=a[i];
    }
    if(c==a)cout<<"yes";
    else cout<<"no";
	return 0;
}