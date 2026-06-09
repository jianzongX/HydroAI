#include<bits/stdc++.h>
using namespace std;
char a[505];
int main(){
    for(int i=0;i<505;i++){
        char b[100]={0};
        cin>>b;
        if(b[0]==0)break;
        int len=strlen(b);
        for(int i=len-1;i>=0;i--){
            cout<<b[i];
        }
        cout<<" ";
    }
	return 0;
}