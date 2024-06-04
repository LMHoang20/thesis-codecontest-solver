#include <bits/stdc++.h>
using namespace std;

struct Event {
    int type, x, y, val;
    Event(int a, int b, int c, int d) : type(a), x(b), y(c), val(d) {}
};

int queryBit(vector<int>& bit, int ind) {
    int ans = 0;
    while (ind > 0) {
        ans += bit[ind];
        ind -= ind & -ind;
    }
    return ans;
}

void updateBit(vector<int>& bit, int ind, int val) {
    while (ind < bit.size()) {
        bit[ind] += val;
        ind += ind & -ind;
    }
}

map<int, int> lmap, rmap;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<Event> list;

    vector<int> p(n), s(n), b(n);
    for (int i = 0; i < n; ++i) cin >> p[i];
    for (int i = 0; i < n; ++i) cin >> s[i];
    for (int i = 0; i < n; ++i) cin >> b[i];

    for (int i = 0; i < n; ++i) {
        list.emplace_back(0, p[i], b[i] + p[i], 1);
        list.emplace_back(0, s[i] + 1, b[i] + p[i], -1);
        list.emplace_back(1, p[i], b[i] + 1 - p[i], -1);
        list.emplace_back(1, s[i] + 1, b[i] + 1 - p[i], 1);
    }

    vector<int> inc(m), pb(m);
    for (int i = 0; i < m; ++i) cin >> inc[i];
    for (int i = 0; i < m; ++i) cin >> pb[i];

    for (int i = 0; i < m; ++i) {
        lmap[pb[i] + inc[i]] = 1;
        rmap[pb[i] - inc[i]] = 1;
        list.emplace_back(2, inc[i], pb[i], i);
    }

    sort(list.begin(), list.end(), [](const Event& e1, const Event& e2) {
        if (e1.x != e2.x) return e1.x < e2.x;
        if (e1.type != e2.type) return e1.type < e2.type;
        return false;
    });

    int ptr = 1;
    for (auto& [key, value] : lmap) {
        lmap[key] = ptr++;
    }
    vector<int> lbit(ptr);

    ptr = 1;
    for (auto& [key, value] : rmap) {
        rmap[key] = ptr++;
    }
    vector<int> rbit(ptr);

    vector<int> ans(m);
    for (const Event& e : list) {
        int type = e.type;

        if (type == 0) {
            auto it = lmap.upper_bound(e.y - 1);
            if (it != lmap.end()) {
                updateBit(lbit, it->second, e.val);
            }
        } else if (type == 1) {
            auto it = rmap.upper_bound(e.y - 1);
            if (it != rmap.end()) {
                updateBit(rbit, it->second, e.val);
            }
        } else {
            int lind = lmap[e.y + e.x];
            int rind = rmap[e.y - e.x];
            int ind = e.val;

            ans[ind] = queryBit(lbit, lind) + queryBit(rbit, rind);
        }
    }

    for (int i : ans) {
        cout << i << " ";
    }
    cout << endl;

    return 0;
}
