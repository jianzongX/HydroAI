#include <bits/stdc++.h>
using namespace std;
double b[15]={0,28.9,32.7,45.6,78,35,86.2,27.8,43,56,65};
int main()
{
	double ans=0.0;
    int n;
	for(int i=1;i<=10;i++)
	{
    scanf("%d",&n);
    ans+=n*b[i];
	}
    printf("%0.1lf\n",ans);
	return 0;
}