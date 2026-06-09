#include <iostream>
#include <cmath>
#include <cstdio>

using namespace std;

double x,ans = 1;//它最后还加了个一
int n;

int main(){
	cin >> x >> n;
	for (int i = 1;i <= n; ++ i){
		ans += pow (x,i);
	}
	printf ("%.2f\n",ans);//保留两位小数
	return 0;
}