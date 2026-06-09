#include <bits/stdc++.h>
using namespace std;
int a[10000];
int main()
{
	int b,c;
    for(int i=1;i<=10;i++)cin>>a[i];
    cin>>b;
    for(int i=1;i<=10;i++){
        if(a[i]<=b+30){
            c++;
        }
    }
    cout<<c;
	return 0;
}