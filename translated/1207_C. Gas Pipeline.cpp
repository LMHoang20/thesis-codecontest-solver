```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const ll INF = 1e18;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n, a, b;
    cin >> n >> a >> b;
    string s;
    cin >> s;

    vector<vector<ll>> dp(n + 1, vector<ll>(2, INF));
    dp[0][0] = b;

    for (int i = 0; i < n; i++) {
      if (s[i] == '0') {
        dp[i + 1][0] = min(dp[i + 1][0], dp[i][0] + a + b);
        dp[i + 1][1] = min(dp[i + 1][1], dp[i][0] + 2 * (a + b));

        dp[i + 1][1] = min(dp[i + 1][1], dp[i][1] + a + 2 * b);
        dp[i + 1][0] = min(dp[i + 1][0], dp[i][1] + 2 * a + b);
      } else {
        dp[i + 1][1] = min(dp[i + 1][1], dp[i][1] + a + 2 * b);
      }
    }
    cout << dp[n][0] << endl;
  }
  return 0;
}
```