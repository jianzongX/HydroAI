#include<bits/stdc++.h>
using namespace std;
int a[1000][1000],n,m,sx=1,sy=1,x=1,y=1,num=1,o=0;
int main() {
    cin>>n>>m;
    for(;num<=n*m;){
        o=0;
        a[x][y]=num;num++;
        if(x+1==n+1){o++;
            if(sy+1==m+1)sx++;
            else {sy++;}x=sx;y=sy;
            continue;
        }
        else x++;
        if(y-1==0){
            if(sy+1==m+1)sx++;
            else {sy++;}x=sx;y=sy;
        }
        else {y--;}
    }
    for(int s=1; s<=n; s++) {
		for(int b=1; b<=m; b++) {
			cout<<a[s][b]<<" ";
		}
		cout<<endl;
	}
	return 0;
}