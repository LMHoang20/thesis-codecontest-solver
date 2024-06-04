```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAXN = 100000;

int n, m, d;
bool marked[MAXN];
vector<int> adj[MAXN];
int maxDistanceDown[MAXN];
int maxDistanceUp[MAXN];

void dfs1(int v, int p) {
    maxDistanceDown[v] = marked[v] ? 0 : -1;
    for (int u : adj[v]) {
        if (u == p) continue;
        dfs1(u, v);
        if (maxDistanceDown[u] > -1)
            maxDistanceDown[v] = max(maxDistanceDown[v], maxDistanceDown[u] + 1);
    }
}

void dfs2(int v, int p) {
    int mx1 = -1, mx2 = -1;
    for (int u : adj[v]) {
        if (u == p) continue;
        if (maxDistanceDown[u] > mx1) {
            mx2 = mx1;
            mx1 = maxDistanceDown[u];
        } else if (maxDistanceDown[u] > mx2) {
            mx2 = maxDistanceDown[u];
        }
    }

    for (int u : adj[v]) {
        if (u == p) continue;
        int siblingDistance = maxDistanceDown[u] == mx1 ? mx2 : mx1;
        if (siblingDistance != -1)
            siblingDistance += 2;
        maxDistanceUp[u] = siblingDistance;
        if (maxDistanceUp[v] != -1)
            maxDistanceUp[u] = max(maxDistanceUp[u], maxDistanceUp[v] + 1);
        if (marked[u])
            maxDistanceUp[u] = max(maxDistanceUp[u], 0);
        dfs2(u, v);
    }
}

int main() {
    cin >> n >> m >> d;

    for (int i = 0; i < m; i++) {
        int p;
        cin >> p;
        marked[p - 1] = true;
    }

    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        a--;
        b--;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    dfs1(0, -1);
    maxDistanceUp[0] = marked[0] ? 0 : -1;
    dfs2(0, -1);

    int ans = 0;
    for (int i = 0; i < n; i++) {
        ans += (maxDistanceUp[i] <= d && maxDistanceDown[i] <= d);
    }
    cout << ans << endl;

    return 0;
}
```