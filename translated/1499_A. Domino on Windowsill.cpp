```cpp
#include <iostream>

using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n, k1, k2, w, b;
    cin >> n >> k1 >> k2 >> w >> b;

    if (k1 + k2 >= 2 * w && (n - k1) + (n - k2) >= 2 * b)
      cout << "YES" << endl;
    else
      cout << "NO" << endl;
  }
  return 0;
}
```