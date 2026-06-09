#include<bits/stdc++.h>
using namespace std;
string x,y;
int main(){
    cin>>x>>y;
    if(x.size()<y.size()){
        string my=y+y;
        if(my.find(x)==string::npos){
            cout<<"false";
        }
        else cout<<"true";
    }
    else{
        string mx=x+x;
        if(mx.find(y)==string::npos){
            cout<<"false";
        }
        else cout<<"true";
    }
	return 0;
}