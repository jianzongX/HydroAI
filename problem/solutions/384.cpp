#include<bits/stdc++.h>
using namespace std;
char a[505],b[505];
double c=0.0;
int main(){
    int x;
    cin>>c;
    cin.get();
    cin.get(a,505);
    cin.get();
    cin.get(b,505);
    int len=strlen(a);
    for(int i=0;i<len;i++){
        if(a[i]==b[i])x++;
    }
    if(x/(len*1.0)>=c)cout<<"yes";
    else cout<<"no";
	return 0;
}