#include<bits/stdc++.h>
using namespace std;
char a[205],b,c;
int main(){
    cin.get(a,205);
    cin.get();
    cin>>b>>c;
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]==b){a[i]=c;}
        cout<<a[i];
    }
	return 0;
}