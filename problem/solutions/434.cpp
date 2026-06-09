#include<bits/stdc++.h>
using namespace std;
int main()
{
	int a[105],b[105],m=0,n=0;
	for(int i=0;i<10;i++){
		int x;
		cin>>x;
		if(x%2==0){
			a[m++]=x;
		}
		else
			b[n++]=x;
	}
	sort(a,a+m);
	sort(b,b+n);//sort：排序函数
	for(int i=n-1;i>=0;i--){
		cout<<b[i]<<" ";
	}
	for(int i=0;i<m;i++){
		cout<<a[i]<<" ";
	}
	cout<<endl;
	return 0;
}