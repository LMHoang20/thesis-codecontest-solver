```cpp
#include <bits/stdc++.h>
using namespace std;
const int N = 105, M = 105;
int n, m, l[N][M], r[N][M], dp[M][M];
int main() {
  cin >> n >> m;
  for (int i = 1; i <= n; i++) {
    int k;
    cin >> k;
    for (int j = 1; j <= k; j++) {
      int a, b;
      cin >> a >> b;
      for (int x = a; x <= b; x++) {
        l[i][x] = a, r[i][x] = b;
      }
    }
  }
  for (int i = m; i >= 1; i--) {
    for (int j = i; j <= m; j++) {
      for (int x = i; x <= j; x++) {
        int cnt = 0;
        for (int y = 1; y <= n; y++) {
          if (l[y][x] >= i && r[y][x] <= j) cnt++;
        }
        dp[i][j] = max(dp[i][j], dp[i][x - 1] + cnt * cnt + dp[x + 1][j]);
      }
    }
  }
  cout << dp[1][m] << endl;
  return 0;
}
```