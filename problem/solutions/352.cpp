#include <bits/stdc++.h>
using namespace std;
int main()
{
    int n,cnt=0;
	cin>>n;
	for(int a=2;;a++)
	{
		bool flag=true;
        for(int i=2;i<=sqrt(a);i++)
        if(a%i==0){
            flag=false;
            break;
        }
        if(flag)cnt++;
        if(cnt==n){
            cout<<a<<endl;
            break;
        }
	}
	return 0;
}