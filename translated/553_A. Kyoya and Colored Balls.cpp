```cpp
#include <iostream>
#include <vector>

using namespace std;

const int mod = 1000000007;
const int MAXN = 1010;

long long comb[MAXN][MAXN];

int main() {
  comb[0][0] = 1;
  for (int i = 1; i < MAXN; i++) {
    comb[i][0] = 1;
    for (int j = 1; j <= i; j++) {
      comb[i][j] = (comb[i - 1][j] + comb[i - 1][j - 1]) % mod;
    }
  }

  int K;
  cin >> K;
  vector<int> color(K);
  for (int i = 0; i < K; i++) cin >> color[i];

  long long res = 1;
  int total = 0;
  for (int i = 0; i < K; i++) {
    res = (res * comb[total + color[i] - 1][color[i] - 1]) % mod;
    total += color[i];
  }

  cout << res << endl;
  return 0;
}
```