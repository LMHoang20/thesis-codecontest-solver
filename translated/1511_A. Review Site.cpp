```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    int n;
    cin >> n;
    vector<int> r(n);
    for (int i = 0; i < n; i++) { cin >> r[i]; }
    int ans = 0;
    for (int i = 0; i < n; i++) {
      if (r[i] != 2) { ans++; }
    }
    cout << ans << endl;
  }
  return 0;
}
```