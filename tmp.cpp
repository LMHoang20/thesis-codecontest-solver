#include <bits/stdc++.h>

using namespace std;

const int MAX_WIDTH = 10000;
const int QUERIES = 5;
const long long INF = 2e18;
vector<vector<long long>> memo(QUERIES + 1, vector<long long>(MAX_WIDTH + 1, 0));

long long dp(int guesses, long long l) {
    if (guesses == 0) {
        return l;
    }
    if (l > MAX_WIDTH) {
        return min(INF, dp(guesses, MAX_WIDTH) + l - MAX_WIDTH);
    }
    if (memo[guesses][l] != 0) {
        return memo[guesses][l];
    }
    long long ans = l;
    for (int i = 0; i < l; ++i) {
        ans = dp(guesses - 1, ans);
        ++ans;
    }
    ans = dp(guesses - 1, ans);
    return memo[guesses][l] = min(ans, INF);
}

void run() {
    long long l = 1;
    long long r = dp(QUERIES, 1);
    for (int queriesNext = QUERIES - 1; queriesNext >= 0; --queriesNext) {
        vector<long long> query;
        long long curL = l;
        for (int i = 0, e = min(static_cast<int>(l), MAX_WIDTH); i < e; ++i) {
            long long end = dp(queriesNext, curL);
            query.push_back(end);
            curL = end + 1;
        }
        assert(r == dp(queriesNext, curL));
        cout << query.size();
        for (long long x : query) {
            cout << " " << x;
        }
        cout << endl;
        cout.flush();
        cin.clear();
        int ans;
        cin >> ans;
        if (ans < 0) {
            return;
        }
        if (ans > 0) {
            l = query[ans - 1] + 1;
        }
        if (ans != query.size()) {
            r = query[ans];
        }
        assert(dp(queriesNext, l) == r);
    }
}

int main() {
    run();
    return 0;
}