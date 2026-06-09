#include <bits/stdc++.h>

using namespace std;

priority_queue<int> ma_hp;//大顶堆 
priority_queue<int, vector<int>, greater<int> > mi_hp;//小顶堆 

int n, w, now, num;

void qwq()//调整获奖人数（小顶堆元素个数）
{
	if (mi_hp.size()<now)
	{
		mi_hp.push(ma_hp.top());
		ma_hp.pop();
	} 
	if (mi_hp.size() > now)
	{
		ma_hp.push(mi_hp.top());
		mi_hp.pop();
	}
	
} 

void push(int num)
{
	if (num >= ma_hp.top()) mi_hp.push(num);
		else ma_hp.push(num);
	qwq();
}

int main()
{
	scanf("%d%d", &n, &w);
	ma_hp.push(0);//避免边界判断 
	for (int p = 1; p <= n; p++)
	{
		now=max(1,p*w/100);;//实时获奖人数 
		scanf("%d", &num);
		push(num);
		printf("%d ", mi_hp.top()); 
	}
	return 0;
}