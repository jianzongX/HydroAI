#include <bits/stdc++.h>
using namespace std;
int main(){
	int n,a,b,t;
	cin >>a>>b>>n;
	for(int i=1;i<=n;i++)
	{ 
	  a*= 10;
	  t=a/b;
	  a%=b;
	}
	cout<<t<<endl;
  return 0;
}