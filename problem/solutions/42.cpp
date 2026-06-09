#include<iostream>
#include<cstdio>
#include<cmath>
using namespace std;
int main(){
	int a;
	cin>>a;
    if(a>0){
    	cout<<"positive";
	}
	else{
		if(a<0){
			cout<<"negative";
		}
		else{
			cout<<"zerozero";
		}
	}
	return 0;
}