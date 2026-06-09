#include <bits/stdc++.h>
using namespace std;
int x,y,s;
char f;
int main()
{
	cin>>x>>y>>f>>s;
    for(int i=1;i<=y;i++)cout<<f;
    cout<<endl;
	for(int i=1;i<=x-2;i++)
	{
		cout<<f;
        for(int j=1;j<=y-2;j++){
        if(s==0)cout<<" ";
        else cout<<f;  
        }
        cout<<f;
        cout<<endl;
		
	}
    for(int i=1;i<=y;i++)cout<<f;
    cout<<endl;
	return 0;
}