#include<bits/stdc++.h>
using namespace std;
char a[85];
int main(){
    cin.get(a,85);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]>='a'&&a[i]<='y')a[i]+=1;
        if(a[i]>='A'&&a[i]<='Y')a[i]+=1;
        if(a[i]>='z'&&a[i]<='Z')a[i]-='Z'-'A';
        cout<<a[i];
    }
    
	return 0;
}