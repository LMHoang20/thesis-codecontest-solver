```cpp
#include <iostream>
using namespace std;

int main() {
  int t;
  cin >> t;
  for (int ct = 1; ct <= t; ct++) {
    int str, int_, exp;
    cin >> str >> int_ >> exp;
    int minAddStr = max(0, (exp + int_ - str + 2) / 2);
    cout << max(exp - minAddStr + 1, 0) << endl;
  }
}
```