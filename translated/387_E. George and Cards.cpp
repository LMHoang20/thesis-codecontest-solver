#include <bits/stdc++.h>

using namespace std;

void solve() {
    set<int> integers;
    int n, m;
    cin >> n >> m;
    vector<int> pos(n), need(n), t(n, 0);

    integers.insert(-1);
    integers.insert(n);

    for (int i = 0; i < n; i++) {
        int idx;
        cin >> idx;
        pos[idx - 1] = i;
    }

    for (int i = 0; i < m; i++) {
        int idx;
        cin >> idx;
        need[idx - 1] = 1;
    }

    long long ans = 0;
    for (int i = 0; i < n; i++) {
        if (need[i] == 1) {
            integers.insert(pos[i]);
        } else {
            int r, l;
            auto it_r = integers.upper_bound(pos[i]);
            auto it_l = integers.lower_bound(pos[i]);

            r = *it_r - 1;
            l = *prev(it_l) + 1;

            ans += r - l + 1;

            for (int j = r; j >= 0; j -= (j + 1) & -(j + 1))
                ans -= t[j];

            for (int j = l - 1; j >= 0; j -= (j + 1) & -(j + 1))
                ans += t[j];

            for (int j = pos[i]; j < n; j += (j + 1) & -(j + 1))
                t[j]++;
        }
    }
    cout << ans << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t = 1;
    while (t--) {
        solve();
    }
    return 0;
}
