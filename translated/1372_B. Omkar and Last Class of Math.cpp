```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n;
    cin >> n;
    int p = 0;
    for (int m = 2; m * m <= n; m++) {
      if (n % m == 0) {
        p = m;
        break;
      }
    }
    if (p == 0) {
      p = n;
    }
    cout << n / p << " " << n - (n / p) << endl;
  }
  return 0;
}
```