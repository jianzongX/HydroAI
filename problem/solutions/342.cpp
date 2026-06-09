#include<bits/stdc++.h>//头文件
using namespace std;//cin，cout必备的
long long s[11]={},n,k=0,a=1;//数组s,n和转换后的k,再加一个a,作用后面讲
int main()//主程序
{
	memset(s,0,sizeof(n));//清零
	cin>>n;//输入不解释
    for(int i=1;i<=10;i++) s[i]=n/a%10,a*=10;//求出位数后存入数组，具体的就不说了
    a=1000000000;//初始化
    for(int i=1;i<=10;i++) k+=s[i]*a,a/=10;//存入k
    while(k%10==0) k/=10;//倒着看，最后有0就除掉
    cout<<k;//输出不解释
    return 0;//好习惯棒棒哒[恶心][恶心][呕吐][呕吐]
}