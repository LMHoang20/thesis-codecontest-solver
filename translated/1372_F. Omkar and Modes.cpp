#include <bits/stdc++.h>

using namespace std;

void ask(int l, int r) {
    cout << "? " << l << " " << r << endl;
    fflush(stdout);
}

void answer(vector<int>& ans) {
    cout << "!";
    for (int i = 1; i < ans.size(); i++) {
        cout << " " << ans[i];
    }
    cout << endl;
    fflush(stdout);
}

int calculate(int l, int r, vector<int>& ans, unordered_map<int, int>& length) {
    if (l <= r) {
        ask(l, r);
        string line;
        int a, f;
        cin >> a >> f;
        if (length.count(a)) {
            int end = r - f + length[a];
            for (int j = end - length[a] + 1; j <= end; j++) {
                ans[j] = a;
            }
            length.erase(a);
            calculate(l, r - f, ans, length);
            return end;
        } else {
            length[a] = f;
            int j = l;
            while (length.count(a)) {
                j = calculate(j, j + f - 1, ans, length) + 1;
            }
            return calculate(j, r, ans, length);
        }
    } else {
        return l - 1;
    }
}

int main() {
    int n;
    cin >> n;
    vector<int> ans(n + 1);
    unordered_map<int, int> length;
    calculate(1, n, ans, length);
    answer(ans);
    return 0;
}
