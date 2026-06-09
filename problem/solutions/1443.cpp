#include<bits/stdc++.h>
using namespace std;
queue<long long> q1,q2;
int main() {
    long long n;
    cin>>n;
    long long s=n;
    for(long long i=2;i*i<=s;i++){
        if(s%i==0){
            int b=0;
            while(s%i==0){
                b++;
                s/=i;
            }
            q1.push(i);
            q2.push(b);
        }
    }
    if(s>1){
        q1.push(s);
        q2.push(1);
    }
    int i=1;
    while(!q1.empty()){
        long long a1=q1.front();
        q1.pop();
        int a2=q2.front();
        q2.pop();
        if(a2==1&&i!=1)cout<<" * "<<a1;
        else if(a2==1&&i==1)cout<<a1;
        else if(a2>=2&&i!=1)cout<<" * "<<a1<<'^'<<a2;
        else if(a2>=2&&i==1)cout<<a1<<'^'<<a2;
        i++;
    }
    return 0;
}