#include<bits/stdc++.h>
using namespace std;
int main(){
    int a,b,c,count=0;
    cin>>a>>b>>c;
    for(int x=0;x<=c;x++)
    for(int y=0;y<=c;y++){
        if(x*a+y*b==c)
        count++;
    }
    cout<<count<<endl;
	return 0;
}