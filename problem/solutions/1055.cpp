#include<bits/stdc++.h>
using namespace std;
int main(){
    long long n,facn=1;
    cin>>n;
    for(int i=1;i<=n;i++){
    	facn=facn*i;
	}
	cout<<facn<<endl;
	return 0;
}