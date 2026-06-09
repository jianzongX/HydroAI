#include<bits/stdc++.h>
using namespace std;
int n;
int main(){
    cin>>n;
    string a,c[105];
    int k=0;
    for(int i=0;i<n;i++){
        cin>>a;int b=a.size();
        for(int j=0;j<b;j++){
            if(a[j]>='A'&&a[j]<='Z')a[j]+=32;
        }
        if(a[0]>='a'&&a[0]<='z'){a[0]-=32;}
        c[k]=a;k++;
    }
    for(int i=0;i<n;i++){
    	cout<<c[i]<<endl;
	}
	return 0;
}