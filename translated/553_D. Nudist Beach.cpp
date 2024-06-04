#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> graph;
vector<int> deg, cur;
vector<bool> vis;

struct State {
    int node;
    long long val;
    State(int n, int v) : node(n), val(v) {}
    bool operator<(const State& other) const {
        return deg[node] * other.val > val * deg[other.node];
    }
};

long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, K;
    cin >> N >> M >> K;

    vis.resize(N);
    for (int i = 0; i < K; i++) {
        int x;
        cin >> x;
        vis[x - 1] = true;
    }

    deg.resize(N);
    cur.resize(N);
    graph.resize(N);
    for (int i = 0; i < M; i++) {
        int a, b;
        cin >> a >> b;
        a--; b--;
        graph[a].push_back(b);
        graph[b].push_back(a);
        deg[a]++;
        deg[b]++;
        if (vis[a]) cur[b]++;
        if (vis[b]) cur[a]++;
    }

    priority_queue<State> pq;
    for (int i = 0; i < N; i++) {
        if (!vis[i]) {
            pq.emplace(i, cur[i]);
        }
    }

    long long num = 1, den = 1;
    vector<int> lst(N);
    int idx = 0;
    int best = 0;

    while (!pq.empty()) {
        State s = pq.top();
        pq.pop();
        if (cur[s.node] != s.val || vis[s.node]) continue;
        lst[idx++] = s.node;
        long long tn = s.val, td = deg[s.node];
        if (num * td > den * tn) {
            num = tn;
            den = td;
            best = idx - 1;
        }
        vis[s.node] = true;
        for (int neighbor : graph[s.node]) {
            if (!vis[neighbor]) {
                pq.emplace(neighbor, ++cur[neighbor]);
            }
        }
    }

    vector<int> res(idx - best);
    for (int i = best; i < idx; i++) {
        res[i - best] = lst[i] + 1;
    }

    cout << res.size() << '\n';
    for (int i = 0; i < res.size(); i++) {
        if (i != 0) cout << ' ';
        cout << res[i];
    }
    cout << '\n';

    return 0;
}
