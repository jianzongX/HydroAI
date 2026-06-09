#include<bits/stdc++.h>
using namespace std;
double f(double x,double n){
    if(n==1)return x/(n+x);
    return x/(n+f(x,n-1));
}
int main(){
	int a,b;
	cin>>a>>b;
	printf("%.2lf",f(a,b));
	return 0;
}