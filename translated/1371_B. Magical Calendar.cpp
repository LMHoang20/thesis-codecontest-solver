```cpp
#include <iostream>

using namespace std;

int main() {
  long long t, n, r, res;
  cin >> t;
  while (t--) {
    res = 0;
    cin >> n >> r;
    if (n <= 1) {
      cout << "1\n";
      continue;
    }
    if (n <= r) {
      r = n - 1;
      res = 1;
    }
    cout << res + ((1 + r) * (r - 1 + 1)) / 2 << "\n";
  }
  return 0;
}
```