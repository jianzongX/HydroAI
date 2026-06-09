#include <bits/stdc++.h>
using namespace std;
int n;
int main()
{
	cin>>n;
	for(int i=1;i<=n;i++)
	{
        for(int v=1;v<=n-i;v++){
            cout<<" ";
        }
		for(int j=1;j<=i*2-1;j++)
		cout<<"*";
		cout<<endl;
	}
	return 0;
}