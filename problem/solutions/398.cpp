#include<bits/stdc++.h>
using namespace std;
int b=1;
char a[1005];
int main(){
    cin>>a;
    for(int i=0;i<strlen(a);i++){
        if(a[i]==a[i+1])b++;
        else{
            cout<<b<<a[i];
            b=1;
        }
    }
	return 0;
}