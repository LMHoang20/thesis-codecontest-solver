```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n, k;
    cin >> n >> k;
    if (k % n == 0) {
      cout << "0\n";
    } else {
      cout << "2\n";
    }
    vector<vector<int>> grid(n, vector<int>(n, 0));
    int p = 0, q = 0;
    while (k > 0) {
      k--;
      grid[p][q] = 1;
      p++;
      q++;
      q %= n;
      if (p == n) {
        p = 0;
        q++;
        q %= n;
      }
    }
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        cout << grid[i][j];
      }
      cout << endl;
    }
  }
  return 0;
}
```