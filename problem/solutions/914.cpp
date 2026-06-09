#include<bits/stdc++.h>
using namespace std;
int n;
string a[1005];
char b[1005][1005];
long long c[15];
map<string, int> SS; 
int pd(long long aa,long long bb,long long cc){
	if(aa<=bb&&bb<=cc)return 0;
	return 1; 
}
int pd0(const char* ip) {
//    string s = ip;
//    string str="";
//    int k=5,i=0; 
//    while(k--){
//    	if(s[i]=='.'||s[i]==':'||s[i]=='\0'){
//    		i+=2;
//    		int len1=str.size();
//    		int len2=1+log10(stoi(str));
//    		if(len1!=len2)return 1;
//		}
//		else {
//		    str+=s[i];	
//		    i++;
//		}
//	}
//	return 0;

//    for(int i = 0; i <= s.size(); i++) {
//        if(s[i] == '.' || s[i] == ':' || s[i] == '\0') {
//            int len = i - start;
//            if(len > 1 && s[start] == '0') return 1;
//            if(len == 0) return 1;
//            start = i + 1;
//        }
//    }
string s = ip;
    int start = 0;
    int segments = 0;
    
    for(int i = 0; i <= s.size(); i++) {
        if(s[i] == '.' || s[i] == ':' || i == s.size()) {
            int len = i - start;
            if(len == 0) return 1;
            if(segments < 5) {
                if(len > 1 && s[start] == '0') {
                    return 1;
                }
            }
            start = i + 1;
            segments++;
        }
    }
    
    return 0;
    return 0;
}
int main() {
    freopen("network.in", "r", stdin);
    freopen("network.out", "w", stdout);
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i]>>b[i];
        int l=sscanf(b[i],"%lld.%lld.%lld.%lld:%lld",&c[1],&c[2],&c[3],&c[4],&c[5]);
        int dh=0,mh=0;

        for(int j=0;j<=strlen(b[i]);j++){
        	if(b[i][j]=='.')dh++;
        	if(b[i][j]==':')mh++;
		}
		if(dh>3||mh>1){
			cout<<"ERR"<<endl;
        	continue; 
		} 
        if(l!=5){
        	cout<<"ERR"<<endl;
        	continue;
		}
        if(pd0(b[i])) {
            cout << "ERR" << endl;
            continue;
        }
        
		if(pd(0,c[1],255)||pd(0,c[2],255)||pd(0,c[3],255)||pd(0,c[4],255)||pd(0,c[5],65535)){
			cout<<"ERR"<<endl;
        	continue;
		}
        if (a[i] == "Server") {
            if (SS.find(b[i]) == SS.end()){
                SS[b[i]] = i;
                cout << "OK" << endl;
            }
			else cout << "FAIL" << endl;
        } if (a[i] == "Client") {
            if (SS.find(b[i]) != SS.end())cout << SS[b[i]] << endl;
			else cout << "FAIL" << endl;
        }
    }
    return 0;
}