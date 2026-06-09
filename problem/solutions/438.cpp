#include<bits/stdc++.h>
using namespace std;
int main(){
    string a[105];
    int x=0;
    for(int i=0;i<305;i++){
        string b;
        cin>>b;
        int len=b.size();
        if(len==0)break;
        a[i]=b;x++;
    }
    for(int i=0;i<x;i++){
        for(int j=i+1;j<x;j++){
            if(a[i]>a[j]){
                swap(a[i],a[j]);
        }
    }
    }
    for(int i=0;i<x;i++){
        cout<<a[i]<<endl;
    }
	return 0;
}