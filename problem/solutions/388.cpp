#include<bits/stdc++.h>
using namespace std;
char a[260];
int main(){
    cin.get(a,260);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]=='A'){a[i]='T';continue;}
        if(a[i]=='T'){a[i]='A';continue;}
        if(a[i]=='G'){a[i]='C';continue;}
        if(a[i]=='C'){a[i]='G';continue;}
    }
    for(int i=0;i<len;i++){
        cout<<a[i];
    }
	return 0;
}