#include<bits/stdc++.h>
using namespace std;
int main(){
    unsigned int a,b;
    cin>>a;
    b=a<<16;
    cout<<b+(a>>16);
	return 0;
}