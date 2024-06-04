```cpp
#include <bits/stdc++.h>

using namespace std;

const int INF = 1e9 + 7;

int main() {
  string s;
  cin >> s;
  int cf[10][10] = {};
  for (int i = 1; i < s.size(); i++) cf[s[i - 1] - '0'][s[i] - '0']++;
  for (int x = 0; x < 10; x++) {
    for (int y = 0; y < 10; y++) {
      int ds[10][10];
      for (int i = 0; i < 10; i++) fill(ds[i], ds[i] + 10, INF + 7);
      for (int v = 0; v < 10; v++) {
        for (int cx = 0; cx < 10; cx++) {
          for (int cy = 0; cy < 10; cy++) {
            if (cx + cy == 0) continue;
            int to = (v + cx * x + cy * y) % 10;
            ds[v][to] = min(ds[v][to], cx + cy);
          }
        }
      }
      int res = 0;
      for (int v = 0; v < 10; v++) {
        for (int to = 0; to < 10; to++) {
          if (ds[v][to] > INF && cf[v][to] > 0) {
            res = -1;
            break;
          }
          res += (ds[v][to] - 1) * cf[v][to];
        }
        if (res == -1) break;
      }
      cout << res << " ";
    }
    cout << endl;
  }
  return 0;
}
```