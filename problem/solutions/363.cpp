#include <bits/stdc++.h>
using namespace std;
double a[10005];
int main()
{
	int b,c,d;
    cin>>b;
    for(int i=1;i<=b;i++)cin>>a[i];
    cin>>c;
    for(int i=1;i<=b;i++){
        if(c==a[i]){
            d=i;
            break;
        }
    }
    cout<<d;
	return 0;
}