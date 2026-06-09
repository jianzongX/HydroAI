#include<bits/stdc++.h>
using namespace std;
void f(int x){
    if(x<10){
        cout<<x;
        return;
    }
    cout<<x%10;
    f(x/10);
}
int main(){
	int n;
    cin>>n;
    f(n);
	return 0;
}