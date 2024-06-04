#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1048576;

int max(int a, int b) { return (a > b) ? a : b; }

struct STNode {
    int str[2][2];
    int res;
    int dvd;
};

STNode stree[2 * MAXN][2], vd;
int fl[2 * MAXN];

STNode merge(STNode l, STNode r) {
    STNode res;
    res.res = max(l.res, r.res);
    if (l.dvd == 1 && r.dvd == 1) {
        res.str[0][0] = l.str[0][0];
        res.str[0][1] = l.str[0][1];
        if (l.str[1][1] != 0 && r.str[0][0] != 0) {
            res.res = max({ l.str[1][0] + l.str[1][1], r.str[0][0] + r.str[0][1], res.res });
        } else {
            res.res = max(l.str[1][0] + l.str[1][1] + r.str[0][0] + r.str[0][1], res.res);
        }
        res.str[1][0] = r.str[1][0];
        res.str[1][1] = r.str[1][1];
        res.dvd = 1;
    } else if (l.dvd == 1 && r.dvd == 0) {
        res.str[0][0] = l.str[0][0];
        res.str[0][1] = l.str[0][1];
        if (l.str[1][1] != 0 && r.str[0][0] != 0) {
            res.res = max(l.str[1][0] + l.str[1][1], res.res);
            res.str[1][0] = r.str[0][0];
            res.str[1][1] = r.str[0][1];
        } else {
            res.str[1][0] = l.str[1][0] + r.str[0][0];
            res.str[1][1] = l.str[1][1] + r.str[0][1];
        }
        res.dvd = 1;
    } else if (l.dvd == 0 && r.dvd == 1) {
        if (l.str[0][1] != 0 && r.str[0][0] != 0) {
            res.res = max(r.str[0][0] + r.str[0][1], res.res);
            res.str[0][0] = l.str[0][0];
            res.str[0][1] = l.str[0][1];
        } else {
            res.str[0][0] = l.str[0][0] + r.str[0][0];
            res.str[0][1] = l.str[0][1] + r.str[0][1];
        }
        res.str[1][0] = r.str[1][0];
        res.str[1][1] = r.str[1][1];
        res.dvd = 1;
    } else {
        if (l.str[0][1] != 0 && r.str[0][0] != 0) {
            res.str[0][0] = l.str[0][0];
            res.str[0][1] = l.str[0][1];
            res.str[1][0] = r.str[0][0];
            res.str[1][1] = r.str[0][1];
            res.dvd = 1;
        } else {
            res.str[0][0] = l.str[0][0] + r.str[0][0];
            res.str[0][1] = l.str[0][1] + r.str[0][1];
            res.str[1][0] = 0;
            res.str[1][1] = 0;
            res.dvd = 0;
        }
    }
    return res;
}

void segment_tree_init() {
    for (int i = (MAXN - 2); i >= 0; i--) {
        stree[i][0] = merge(stree[i * 2 + 1][0], stree[i * 2 + 2][0]);
        stree[i][1] = merge(stree[i * 2 + 1][1], stree[i * 2 + 2][1]);
    }
    fill(begin(fl), end(fl), 0);
}

void eval(int k) {
    if (fl[k] % 2 == 1) {
        swap(stree[k][0], stree[k][1]);
        if (k < (MAXN - 1)) {
            fl[k * 2 + 1]++;
            fl[k * 2 + 2]++;
        }
    }
    fl[k] = 0;
}

void rev_query(int a, int b, int k, int l, int r) {
    eval(k);
    if (r <= a || b <= l) return;
    if (a <= l && r <= b) {
        fl[k]++;
        eval(k);
        return;
    }
    eval(k * 2 + 1);
    eval(k * 2 + 2);
    rev_query(a, b, k * 2 + 1, l, (l + r) / 2);
    rev_query(a, b, k * 2 + 2, (l + r) / 2, r);
    stree[k][0] = merge(stree[k * 2 + 1][0], stree[k * 2 + 2][0]);
    stree[k][1] = merge(stree[k * 2 + 1][1], stree[k * 2 + 2][1]);
    fl[k] = 0;
}

STNode get_query(int a, int b, int k, int l, int r) {
    eval(k);
    if (r <= a || b <= l) return vd;
    if (a <= l && r <= b) return stree[k][0];
    STNode ld = get_query(a, b, k * 2 + 1, l, (l + r) / 2);
    STNode rd = get_query(a, b, k * 2 + 2, (l + r) / 2, r);
    return merge(ld, rd);
}

int main() {
    vd.str[0][0] = 0; vd.str[0][1] = 0;
    vd.str[1][0] = 0; vd.str[1][1] = 0;
    vd.res = 0; vd.dvd = 0;
    STNode tl, tr;
    tl.str[0][0] = 0; tl.str[0][1] = 1;
    tl.str[1][0] = 0; tl.str[1][1] = 0;
    tl.res = 0; tl.dvd = 0;
    tr.str[0][0] = 1; tr.str[0][1] = 0;
    tr.str[1][0] = 0; tr.str[1][1] = 0;
    tr.res = 0; tr.dvd = 0;

    int n, q, l, r, ans;
    STNode res;
    string s;
    cin >> n >> q >> s;
    s = " " + s;  // To match 1-based indexing

    for (int i = 0; i < 2 * MAXN; i++) {
        stree[i][0] = vd;
        stree[i][1] = vd;
    }
    for (int i = 1; i <= n; i++) {
        if (s[i] == '<') {
            stree[i + (MAXN - 1)][0] = tl;
            stree[i + (MAXN - 1)][1] = tr;
        } else {
            stree[i + (MAXN - 1)][0] = tr;
            stree[i + (MAXN - 1)][1] = tl;
        }
    }
    segment_tree_init();

    while (q--) {
        cin >> l >> r;
        rev_query(l, r + 1, 0, 0, MAXN);
        res = get_query(l, r + 1, 0, 0, MAXN);
        ans = max(res.str[0][0] + res.str[0][1], res.str[1][0] + res.str[1][1]);
        ans = max(res.res, ans);
        cout << ans << endl;
    }

    return 0;
}
