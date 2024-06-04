```cpp
#include <iostream>

using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    long long r, b, d;
    cin >> r >> b >> d;
    cout << (min(r, b) * (d + 1) >= max(r, b) ? "YES" : "NO") << endl;
  }
  return 0;
}
```