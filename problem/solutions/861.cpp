#include <bits/stdc++.h>	
using namespace std;
int n, y, x, s;
int main()
{
	int n,s=0,x,y;
	x=1;y=1;
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		s+=x;
		y--;
		if(y==0)
		{
			x++;
			y=x;
		}
	}
	cout<<s;
	return 0;
}