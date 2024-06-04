#include <bits/stdc++.h>

using namespace std;

const int MOD = 1000000007;
const int MAXN = 100000;
struct Edge {
    int from, to;
    Edge(int from, int to) : from(from), to(to) {}
};

vector<int> graph[MAXN];
vector<Edge> zeros, ones;
int par[MAXN], sz[MAXN];
bool vis[MAXN], color[MAXN];

int find(int x) {
    return x == par[x] ? x : (par[x] = find(par[x]));
}

void join(int a, int b) {
    int x = find(a), y = find(b);
    if (x == y) return;
    if (sz[x] < sz[y]) swap(x, y);
    par[y] = x;
    sz[x] += sz[y];
}

bool dfs(int node, bool c) {
    if (vis[node]) return c == color[node];
    vis[node] = true;
    color[node] = c;
    for (int neighbor : graph[node]) {
        if (!dfs(neighbor, !c))
            return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int N, M;
    cin >> N >> M;
    zeros.clear();
    ones.clear();
    for (int i = 0; i < M; i++) {
        int a, b, c;
        cin >> a >> b >> c;
        a--; b--;
        if (c == 0) {
            zeros.emplace_back(a, b);
        } else {
            ones.emplace_back(a, b);
        }
    }

    for (int i = 0; i < N; i++) {
        par[i] = i;
        sz[i] = 1;
    }

    for (const Edge &e : ones) {
        join(e.from, e.to);
    }

    for (int i = 0; i < N; i++) graph[i].clear();

    for (const Edge &e : zeros) {
        graph[find(e.from)].push_back(find(e.to));
        graph[find(e.to)].push_back(find(e.from));
    }

    memset(vis, false, N * sizeof(bool));
    memset(color, false, N * sizeof(bool));

    int comp = 0;
    for (int i = 0; i < N; i++) {
        if (find(i) == i && !vis[i]) {
            if (!dfs(i, false)) {
                cout << 0 << endl;
                return 0;
            } else {
                comp++;
            }
        }
    }

    int res = 1;
    for (int i = 0; i < comp - 1; i++) res = (res * 2) % MOD;

    cout << res << endl;
    
    return 0;
}
