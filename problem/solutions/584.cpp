#include<bits/stdc++.h>
using namespace std;
int a,b,n;
int main(){
    cin>>a>>b>>n;
    int i=1,x=1,y=1;
    while(i!=n+1){
        if(x==a+1)x=1;
        if(y==b+1)y=1;
        cout<<x<<' '<<y<<endl;
        x++;
        y++;
        i++;
    }
	return 0;
}