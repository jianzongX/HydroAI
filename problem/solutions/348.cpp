#include<bits/stdc++.h> 
using namespace std;
int main(){
	int n;
	int a=0;
	cin>>n;
	for(int i=1;i<=n;i++){
		int j=i;
		while(j){
			if(j%10==1){
				a++;
			}
			j /= 10;
		}
	}
	cout<<a<<endl;
	return 0;
}