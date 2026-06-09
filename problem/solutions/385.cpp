#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;cin>>n;
    for(int i=0;i<n;i++){
        char a[105],b[105];
        cin>>a>>b;
        if(a[0]=='R'&&b[0]=='S')cout<<"Player1";
        if(a[0]=='S'&&b[0]=='R')cout<<"Player2";
        if(a[0]=='R'&&b[0]=='P')cout<<"Player2";
        if(a[0]=='P'&&b[0]=='R')cout<<"Player1";
        if(a[0]=='P'&&b[0]=='S')cout<<"Player2";
        if(a[0]=='S'&&b[0]=='P')cout<<"Player1";
        if(a[0]==b[0])cout<<"Tie";
        cout<<endl;
    }
    return 0;

}