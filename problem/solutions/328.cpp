#include<bits/stdc++.h>
using namespace std;
int main(){
	int m,n,cnt=0;//cnt是不能取药的人的个数
	cin>>m>>n;
	for(int i=1;i<=n;i++){
		int x;
		cin>>x;
		if(m>=x) m-=x;//可以取药
		else cnt++;//不能取药
	}
	cout<<cnt;
	return 0;
}