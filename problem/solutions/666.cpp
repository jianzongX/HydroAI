#include<bits/stdc++.h>
using namespace std;
int main()
{
	int n;
	cin>>n;
	if(n/4<n%4)
	{
		cout<<0;
		return 0;
	}
	cout<<(n/4-n%4)/5+1;
	return 0;
}