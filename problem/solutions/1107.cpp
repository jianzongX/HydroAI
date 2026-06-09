#include<bits/stdc++.h>
using namespace std;
int a[1000][1000]={0},n,x,y;
int main() {
	cin>>n;
	x=1;y=n;
	for(int i=0;i<=2*n;i++){
		for(int j=0;j<=2*n;j++){
			if(i==0)a[i][j]=-1;
			if(i==2*n)a[i][j]=-1;
			if(j==0)a[i][j]=-1;
			if(j==2*n)a[i][j]=-1;
		}
	}
	for(int num=1;num<=(2*n-1)*(2*n-1);num++){
        a[x][y]=num;
        if(x==1&&y!=(2*n-1)){x=(2*n-1);y=y+1;continue;}
        if(y==(2*n-1)&&x!=1){y=1;x=x-1;continue;}
        if(x==1&&y==(2*n-1)){x=x+1;continue;}
        if(x!=1&&y!=(2*n-1)){
            if(!a[x-1][y+1])x=x-1,y=y+1;
            else x=x+1;
        }
    }
	for(int i=1;i<=2*n-1;i++){
		for(int j=1;j<=2*n-1;j++){
			cout<<a[i][j]<<" ";
		}
		cout<<endl;
	}
	return 0;
}