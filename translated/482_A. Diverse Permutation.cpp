#include <bits/stdc++.h>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<bool> used(n, false);

    int l = 0, r = n - 1;

    for (int i = 0; i < k; ++i) {
        if ((i & 1) == 0) {
            used[l] = true;
            cout << (1 + (l++)) << ' ';
        } else {
            used[r] = true;
            cout << (1 + (r--)) << ' ';
        }
    }

    if ((k & 1) == 1) {
        for (int i = 0; i < n; ++i) {
            if (!used[i]) {
                cout << (i + 1) << ' ';
            }
        }
    } else {
        for (int i = n - 1; i >= 0; --i) {
            if (!used[i]) {
                cout << (i + 1) << ' ';
            }
        }
    }

    cout << '\n';
    return 0;
}
