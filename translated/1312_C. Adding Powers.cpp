```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
  int T;
  cin >> T;
  for (int tc = 1; tc <= T; tc++) {
    long long n, k;
    cin >> n >> k;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) { cin >> a[i]; }

    long long maxPower = 1;
    while (maxPower < 1e16) maxPower *= k;

    bool possible = true;
    while (maxPower > 0) {
      vector<int> positions;
      for (int i = 0; i < n; i++) {
        if (a[i] >= maxPower) positions.push_back(i);
      }
      if (!positions.empty()) {
        if (positions.size() > 1) {
          possible = false;
          break;
        }
        a[positions[0]] -= maxPower;
      }
      maxPower /= k;
    }
    if (!possible || *max_element(a.begin(), a.end()) > 0) {
      cout << "NO" << endl;
    } else {
      cout << "YES" << endl;
    }
  }
  return 0;
}
```