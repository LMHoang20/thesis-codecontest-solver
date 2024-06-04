```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  ll n, x, y;
  cin >> n >> x >> y;
  if (x > y) {
    vector<int> deg(n);
    for (int i = 0; i < n - 1; i++) {
      int a, b;
      cin >> a >> b;
      a--, b--;
      deg[a]++, deg[b]++;
    }
    int mx = 0;
    for (int i = 0; i < n; i++) mx = max(mx, deg[i]);
    cout << y * (n - 2) + (mx == n - 1 ? x : y) << endl;
  } else {
    vector<vector<int>> graph(n);
    for (int i = 0; i < n - 1; i++) {
      int a, b;
      cin >> a >> b;
      a--, b--;
      graph[a].push_back(b);
      graph[b].push_back(a);
    }
    ll ans = 0;
    function<int(int, int)> dfs = [&](int node, int par) {
      int left = 2;
      for (int next : graph[node]) {
        if (next == par) continue;
        int x = dfs(next, node);
        if (left > 0 && x == 1) {
          ans++;
          left--;
        }
      }
      return left > 0 ? 1 : 0;
    };
    dfs(0, -1);
    cout << (n - 1 - ans) * y + ans * x << endl;
  }
  return 0;
}
```