#include<bits/stdc++.h>
using namespace std;
int main() {
	int i=0,k;
	double s=0.0;
	scanf("%d",&k);
	do {
		i++;
		s+=1.0/i;
	}while(s<=k*1.0);
	printf("%d\n",i) ;

}