```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
  string s;
  cin >> s;
  int n = s.length(), j = n - 1, ans = 0;
  while (j >= 0) {
    int k = j;
    while (s[k] == '0')
      k--;
    int len = j - k + 1;

    if (len > k) {
      ans++;
      j = -1;
      continue;
    }

    if (len == k) {
      if (s[0] >= s[k])
        j = k - 1;
      else
        j = -1;
      ans++;
      continue;
    }

    if (len < k) {
      ans++;
      j = k - 1;
    }
  }
  cout << ans << endl;
  return 0;
}
```