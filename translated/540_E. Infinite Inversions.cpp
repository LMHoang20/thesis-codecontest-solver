#include <bits/stdc++.h>

using namespace std;

struct Item {
    int pos, val;

    Item(int pos, int val) : pos(pos), val(val) {}

    bool operator<(const Item& other) const {
        if (pos != other.pos) {
            return pos < other.pos;
        }
        return val < other.val;
    }
};

struct FenwickTree {
    int n;
    vector<int> a;

    FenwickTree(int n) : n(n), a(n, 0) {}

    int sum(int r) {
        int res = 0;
        for (int i = r; i >= 0; i = (i & (i + 1)) - 1) {
            res += a[i];
        }
        return res;
    }

    int sum(int l, int r) {
        return sum(r) - sum(l - 1);
    }

    void inc(int i) {
        for (; i < n; i |= i + 1) {
            a[i]++;
        }
    }
};

void compress(vector<int>& a) {
    set<int> set(a.begin(), a.end());
    map<int, int> map;
    for (int x : set) {
        int id = map.size();
        map[x] = id;
    }
    for (int& x : a) {
        x = map[x];
    }
}

void solve(int testNumber, istream& in, ostream& out) {
    int q;
    in >> q;
    map<int, int> map;
    for (int i = 0; i < q; i++) {
        int pos1, pos2;
        in >> pos1 >> pos2;
        pos1--; // convert to 0-based index
        pos2--; // convert to 0-based index
        int num1 = map.count(pos1) ? map[pos1] : pos1;
        int num2 = map.count(pos2) ? map[pos2] : pos2;
        map[pos1] = num2;
        map[pos2] = num1;
    }
    vector<Item> a;
    for (auto& e : map) {
        a.emplace_back(e.first, e.second);
    }
    int n = a.size();
    vector<int> b(n);
    for (int i = 0; i < n; i++) {
        b[i] = a[i].val;
    }
    compress(b);
    long long ans = 0;
    FenwickTree tree(n);
    for (int i = 0; i < n; i++) {
        ans += tree.sum(b[i], n - 1);
        tree.inc(b[i]);
    }
    for (int idxAfter = 0; idxAfter < n; idxAfter++) {
        int idxBefore = lower_bound(a.begin(), a.end(), Item(a[idxAfter].val, -1)) - a.begin();
        ans += abs(a[idxAfter].pos - a[idxBefore].pos);
        ans -= abs(idxAfter - idxBefore);
    }
    out << ans << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int testNumber = 1;
    solve(testNumber, cin, cout);
    return 0;
}
