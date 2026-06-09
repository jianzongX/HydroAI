#include<bits/stdc++.h>
using namespace std;

int main()
{
    int a,b;
    char c;
	cin>>a>>c;
	if(a<=1000){
	b=8;
	}
	else{
	b=8+ceil((a-1000)/500.0)*4;       
    }
    if(c=='y')
	{
	b=b+5;
	}
	cout<<b;
return 0;
}