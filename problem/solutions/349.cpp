#include<bits/stdc++.h> 
using namespace std;
int main(){
	int n,x;
	int a=0;
	cin>>n>>x;
	for(int i=n;i<=x;i++){
		int j=i;
		while(j){
			if(j%10==2){
				a++;
			}
		j /= 10;
		}
	}
	cout<<a<<endl;
	return 0;
}