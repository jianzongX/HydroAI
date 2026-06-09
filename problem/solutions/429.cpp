#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, k;
    // 定义结构体存储学号和成绩，方便排序
    struct Student {
        int id;     // 学号
        float score;// 成绩
    } stu[105];    // n≤100，留少量冗余即可

    // 输入学生人数n和第k名
    cin >> n >> k;
    // 输入每个学生的学号和成绩
    for (int i = 0; i < n; i++) {
        cin >> stu[i].id >> stu[i].score;
    }

    // 冒泡排序：按成绩从高到低排序（降序）
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (stu[j].score < stu[j+1].score) { // 前 < 后则交换，降序排列
                swap(stu[j], stu[j+1]);
            }
        }
    }

    // 输出第k名（注意k是1-based，数组是0-based，所以取k-1）
    printf("%d %g\n", stu[k-1].id, stu[k-1].score);

    return 0;
}