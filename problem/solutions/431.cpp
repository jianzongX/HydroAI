#include<bits/stdc++.h>
using namespace std;
int main(){
	int a[105],n;
    string b[105];
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>b[i]>>a[i];
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
        swap(b[i],b[id]);
    }
    for(int i=n-1;i>=0;i--){
        for(int j=i+1;j>=0;j--){
            if(a[i]==a[j]){
                if(b[i]<b[j]){
                    swap(a[i],a[j]);
                    swap(b[i],b[j]);
                }
            }
        }
    }
    for(int i=n-1;i>=0;i--){
        cout<<b[i]<<' '<<a[i]<<endl;
    }
	return 0;
}