#include<bits/stdc++.h>
using namespace std;
char a[305];
int main(){
    int o=0;
    for(int i=0;i<305;i++){
        char b[100]={0};
        cin>>b;
        int len=strlen(b);
        if(len==0)break;
        o+=len;
        len=0;
        
    }
    cout<<o;
	return 0;
}