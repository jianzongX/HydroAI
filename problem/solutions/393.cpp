#include<bits/stdc++.h>
using namespace std;
string x,y;
int main(){
    cin>>x>>y;
    if(y.find(x)!=string::npos)cout<<x<<" is substring of "<<y;
    else if(x.find(y)!=string::npos)cout<<y<<" is substring of "<<x;
    else cout<<"No substring";
	return 0;
}