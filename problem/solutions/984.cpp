#include<cstdio>
using namespace std;
int gcd(int x,int y)
{
    if(y==0) return x;
    return gcd(y,x%y);
}
int main()
{
        int i,j,a,b,ansa,ansb,l;
        scanf("%d%d%d",&a,&b,&l);
        ansa=l;ansb=1;
        for(i=1;i<=l;i++)
                for(j=1;j<=l;j++)
                        if(gcd(i,j)==1&&i*b>=j*a&&i*ansb<j*ansa)
                        {
                                ansa=i;
                                ansb=j;
                        }
        printf("%d %d",ansa,ansb);
        return 0;
}