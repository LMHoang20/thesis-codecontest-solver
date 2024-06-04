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
    vector<int> a(n, 1);
    for (int i = 0; i < n; i++) { cout << a[i] << " "; }
    cout << endl;
  }
  return 0;
}
```