```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n, k;
  cin >> n >> k;

  vector<int> a(2 * n);
  for (int i = 0; i < n; i++) {
    if (i > 0) cout << " ";
    if (k > 0) {
      a[2 * i] = 2 * i + 2;
      a[2 * i + 1] = 2 * i + 1;
      k--;
    } else {
      a[2 * i] = 2 * i + 1;
      a[2 * i + 1] = 2 * i + 2;
    }
  }

  for (int i = 0; i < 2 * n; i++) {
    cout << a[i] << " ";
  }
  cout << endl;

  return 0;
}
```