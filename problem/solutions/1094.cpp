#include<bits/stdc++.h>
using namespace std;
int a,b,c;
int main(){
    for(int i=123;i<=333;i++){
        int q[10]={0};
        a=i;b=2*i;c=3*i;
        q[a/100]++;
        q[a/10%10]++;
        q[a%10]++;
        q[b/100]++;
        q[b/10%10]++;
        q[b%10]++;
        q[c/100]++;
        q[c/10%10]++;
        q[c%10]++;
        if(q[1]==1&&q[2]==1&&q[3]==1&&q[4]==1&&q[5]==1&&q[6]==1&&q[7]==1&&q[8]==1&&q[9]==1)cout<<a<<' '<<b<<' '<<c<<endl;
    }
	return 0;
}