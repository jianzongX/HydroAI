#include<bits/stdc++.h>
using namespace std;
int main(){
	long long x,y,z;
	for(x=0;x<=20;x++){	
		for(y=0;y<=100/3;y++){
			for(z=0;z<=100*3;z++){
				if(x+y+z==100 && x*5+y*3+z/3==100&&z%3==0){
					printf("%d %d %d\n",x,y,z);
				}
			}
		}
	}
	return 0;
}