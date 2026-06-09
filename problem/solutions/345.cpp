#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    double a=1.0f;
    long long s=1;
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
    	s=s*i;
    	a=a+1.0/s;
	}
	printf("%.10f",a);
	return 0;
}