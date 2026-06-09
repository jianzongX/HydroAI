#include<bits/stdc++.h>
using namespace std;
priority_queue<int, vector<int>, greater<int> > q;
int x,y,n;
int main(){
	cin>>n;
	for(int i=0;i<n;i++){
		int x;
		cin>>x;
		q.push(x);
	}
	int n=0;
	while(q.size()!=0){
		x=q.top();
		q.pop();
		y=q.top();
		q.pop();
		n+=x+y;
		if(q.size()!=0)q.push(x+y);
		else break;
	}
	cout<<n;
	return 0;
}