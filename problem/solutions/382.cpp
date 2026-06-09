#include<bits/stdc++.h>
using namespace std;
char a[260];
int main(){
	int n=0;
    cin.get(a,260);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]>='0'&&a[i]<='9')n++;
    }
    cout<<n;
	return 0;
}