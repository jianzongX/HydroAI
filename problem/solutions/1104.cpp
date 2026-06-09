#include<bits/stdc++.h>
using namespace std;
char a[205];
int main(){
    cin.get(a,205);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]==' '&&a[i-1]==' ')continue;
        else cout<<a[i];
    }
	return 0;
}