#include<bits/stdc++.h>
using namespace std;
int b=1,x=0;
char a[1005];
int main(){
    cin>>x;
    cin>>a;
    for(int i=0;i<strlen(a);i++){
        if(b==x){cout<<a[i-1];return 0;}
        if(a[i]==a[i+1])b++;
        else{
            b=1;
        }
    }
    cout<<"No";
	return 0;
}