#include <iostream>
using namespace std;
int main()
{
int n,sum = 0;
 cin>>n;
 for (int i=n;i>0;--i){
 int x = 1;
 for(int j=i;j>0;--j){
 x=x*j;
 }
 sum+=x;
 }
 cout<<sum<<endl;
return 0;
}