#include<bits/stdc++.h>
using namespace std;
struct node {
	char x;
	int lc,rc;
} t[300];
void create(int num) {
	if(t[num].x=='.')return;
	create(2*num);
	create(2*num+1);
	cout<<t[num].x;
}
void print(int num) {
    char c;
	cin>>c;
	t[num].x=c;
	if(c=='.')return;
	
	print(2*num);
	cout<<t[num].x;
	print(2*num+1);
}
int main() {
	print(1);
	cout<<endl;
	create(1);
	return 0;
}