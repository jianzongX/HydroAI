#include<bits/stdc++.h>
using namespace std;
int a1=0,a2=0,a3=0,a4=0,a5=0,a6=0;
void m(int n,char A,char B,char C) {
	if(n==0)return;
	m(n-1,A,C,B);
	if(A=='a'&&C=='b')a1++;
	if(A=='a'&&C=='c')a2++;
	if(A=='b'&&C=='a')a3++;
	if(A=='b'&&C=='c')a4++;
	if(A=='c'&&C=='a')a5++;
	if(A=='c'&&C=='b')a6++;
	m(n-1,B,A,C);
}
int main() {
	int n,c;
	cin>>n;
	for(int i=1; i<=n; i++) {
		cin>>c;
		m(c,'a','b','c');
		cout<<"A->B:"<<a1<<endl;
		cout<<"A->C:"<<a2<<endl;
		cout<<"B->A:"<<a3<<endl;
		cout<<"B->C:"<<a4<<endl;
		cout<<"C->A:"<<a5<<endl;
		cout<<"C->B:"<<a6<<endl;
		a1=0;
		a2=0;
		a3=0;
		a4=0;
		a5=0;
		a6=0;
	}
	return 0;
}