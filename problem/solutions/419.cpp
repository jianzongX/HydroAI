#include<bits/stdc++.h>
using namespace std;
double f(double x,double n){
    if(n==1)return sqrt(1+x);
    return sqrt(n+f(x,n-1));
    
}
int main(){
	double a,b;
	cin>>a>>b;
	printf("%.2lf",f(a,b));
	return 0;
}