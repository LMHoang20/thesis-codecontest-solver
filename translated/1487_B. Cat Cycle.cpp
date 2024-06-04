```cpp
#include <iostream>

using namespace std;

int main() {
  int t;
  cin >> t;
  while (t--) {
    long long n, k;
    cin >> n >> k;
    k--;
    long long floor = n / 2;
    cout << ((k + (n % 2) * k / floor) % n + 1) << endl;
  }
  return 0;
}
```