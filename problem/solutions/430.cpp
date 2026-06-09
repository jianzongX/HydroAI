#include<bits/stdc++.h>
using namespace std;
int main(){
	int a[100005],n,x;
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>x;
        if(x%2!=1){i--;n--;}
        else a[i]=x;
    }
    for(int i=0;i<n;i++){
        int minx=0x3f3f3f3f,id=0;
        for(int j=i;j<n;j++){
            if(a[j]<minx){
                minx=a[j];
                id=j;
                }
        }
        swap(a[i],a[id]);
    }
    for(int i=0;i<n-1;i++){
        cout<<a[i]<<',';
    }
    cout<<a[n-1];
	return 0;
}