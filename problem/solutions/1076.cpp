#include <bits/stdc++.h>
using namespace std;
int a,b,c,d;
int main()
{
    for(int i=100;i<=999;i++){
        a=i;
        d=a%10;
        c=(a%100-d)/10;
        b=(a-a%100)/100;
        if(a==pow(d,3)+pow(c,3)+pow(b,3)){
            cout<<a<<endl;
        }
    }
	
	return 0;
}