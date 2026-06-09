#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin >> n;
    vector<pair<int, int> > list;
    for(int i=1;i <= n; i++){
        int a;
        cin >> a;
        list.emplace_back(i, a);
    }
    queue<pair<int, int>> q;
    for(int i = 0; i < n; i++){
        q.push(list[i]);
    }
    while(1){
        queue<pair<int, int> >q1;//当轮选手
        queue<pair<int, int> >q2=q;//复制当前队列
        while(!q2.empty()){
            q1.push(q2.front());
            q2.pop();
        }
        int cp = 0;//晋级人数
        queue<pair<int, int> >jq; //下轮晋级
        while(!q.empty()){
            if(q.size()>=2){
                int id1,p1,id2,p2;
                id1=q.front().first;
                p1=q.front().second;
                q.pop();
                id2=q.front().first;
                p2=q.front().second;
                q.pop();
                if(p1>p2||(p1==p2&&id1<id2))jq.emplace(id1,p1);
                else jq.emplace(id2, p2);
                cp++;
            } 
            else{//轮空
                int id = q.front().first;
                int p = q.front().second;
                q.pop();
                jq.emplace(id, p);
                cp++;
            }
        }
        //倒数第二轮
        if(cp == 2){
            bool first = true;
            while(!q1.empty()){
                if(!first) cout << " ";
                cout << q1.front().second;
                q1.pop();
                first = false;
            }
            cout<<endl;
            return 0;
        }
        // 继续比赛
        q = jq;
    }
    return 0;
}