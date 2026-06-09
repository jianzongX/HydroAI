#include<bits/stdc++.h>
using namespace std;
int n,x=0,a[10005];
int main(){
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    for(int i=0;i<n;i++){
        for(int j=i+1;j<n;j++){
            if(a[i]>a[j]){
                swap(a[i],a[j]);
                x++;
        }
        }
    }
    cout<<x;
	return 0;
}