#include<iostream>
#include<cstdio>
#include<cmath>
using namespace std;
int main()
{
	double a=1,b=1,c,s=0;
	int i,n;
	cin>>n;
	for(i=1;i<=n;++i)
	{
		c=a+b;
		a=b;
		b=c;
		//斐波那契部分； 
		s=s+b/a;//求和； 
	}
	printf("%0.4lf\n",s);
	return 0;
}