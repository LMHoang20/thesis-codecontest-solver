```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

int main() {
  int n, m;
  cin >> n >> m;

  vector<int> deg(m);
  vector<int> p(n);
  for (int i = 0; i < n; ++i) {
    cin >> p[i];
    if (p[i] < m) deg[p[i]]++;
  }

  vector<int> c(n);
  for (int i = 0; i < n; ++i) cin >> c[i];

  int q;
  cin >> q;
  vector<int> qind(q);
  vector<int> vis(n);
  for (int i = 0; i < q; ++i) {
    cin >> qind[i];
    qind[i]--;
    vis[qind[i]] = 1;
  }

  class Kunh {
   public:
    Kunh(int n, vector<int>& deg) {
      pair.resize(n, -1);
      adj.resize(n / 2);
      for (int i = 0; i < n / 2; ++i) {
        adj[i].resize(deg[i]);
      }
      ptr.resize(n / 2);
      vis.resize(n / 2);
    }
    void addEdge(int i, int j) { adj[i][ptr[i]++] = j; }
    bool addFlow(int source) {
      level++;
      return dfs(source);
    }

   private:
    vector<int> pair;
    vector<vector<int>> adj;
    vector<int> ptr;
    vector<int> vis;
    int level = 0;
    bool dfs(int i) {
      vis[i] = level;

      for (int k = 0; k < ptr[i]; ++k) {
        int j = adj[i][k];
        if (pair[j] == -1) {
          pair[j] = i;
          return true;
        } else if (vis[pair[j]] != level && dfs(pair[j])) {
          pair[j] = i;
          return true;
        }
      }

      return false;
    }
  };

  Kunh kunh(2 * m, deg);
  for (int i = 0; i < n; ++i) {
    if (vis[i] == 0) {
      if (p[i] < m) kunh.addEdge(p[i], m + c[i] - 1);
    }
  }
  int ans = 0;
  while (ans < m && kunh.addFlow(ans)) ans++;

  vector<int> fans(q);
  for (int i = q - 1; i >= 0; --i) {
    fans[i] = ans;

    int ind = qind[i];

    if (p[ind] < m) {
      kunh.addEdge(p[ind], m + c[ind] - 1);
    }

    while (ans < m && kunh.addFlow(ans)) ans++;
  }

  for (int i : fans) cout << i << endl;

  return 0;
}
```