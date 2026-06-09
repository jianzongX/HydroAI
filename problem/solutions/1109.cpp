#include<bits/stdc++.h>
using namespace std;
int poww[10][8];
int main(){
    for(int i=0;i<=9;i++){
        for(int j=1;j<=7;j++){
        poww[i][j]=pow(i,j);
    }
    }
    for(int i=100;i<1000;i++){
        if(poww[i/100][3]+poww[i/10%10][3]+poww[i%10][3]==i)cout<<i<<endl;
    }
    for(int i=1000;i<10000;i++){
        if(poww[i/1000][4]+poww[i/100%10][4]+poww[i/10%10][4]+poww[i%10][4]==i)cout<<i<<endl;
    }
    for(int i=10000;i<100000;i++){
        if(poww[i/10000][5]+poww[i/1000%10][5]+poww[i/100%10][5]+poww[i/10%10][5]+poww[i%10][5]==i)cout<<i<<endl;
    }
    for(int i=100000;i<1000000;i++){
        if(poww[i/100000][6]+poww[i/10000%10][6]+poww[i/1000%10][6]+poww[i/100%10][6]+poww[i/10%10][6]+poww[i%10][6]==i)cout<<i<<endl;
    }
    for(int i=1000000;i<10000000;i++){
        if(poww[i/1000000][7]+poww[i/100000%10][7]+poww[i/10000%10][7]+poww[i/1000%10][7]+poww[i/100%10][7]+poww[i/10%10][7]+poww[i%10][7]==i)cout<<i<<endl;
    }
	return 0;
}