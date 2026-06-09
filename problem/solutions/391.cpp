#include<bits/stdc++.h>
using namespace std;
char a[105];
int main(){
    cin.get(a,105);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]>='a'&&a[i]<='z')a[i]-=32;
    }
    for(int i=0;i<len;i++){
        cout<<a[i];
    }
	return 0;
}