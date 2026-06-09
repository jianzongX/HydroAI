#include<bits/stdc++.h>
using namespace std;
int main(){
    char n;//读入的字符
    int k,cnt=0;
    while((n=getchar())!=' ')//终止条件：读入空格（getchar会读空格）
        if(n=='3')
            cnt++;//判断（注意：是字符3）
    cin>>k;//3的个数
    if(cnt==k)
        cout<<"YES";
    else
        cout<<"NO";//判断，输出
    return 0;
}