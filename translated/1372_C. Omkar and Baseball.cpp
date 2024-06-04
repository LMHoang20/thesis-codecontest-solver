```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
  int t;
  cin >> t;
  while (t--) {
    int n;
    cin >> n;
    vector<int> scores(n);
    for (int i = 0; i < n; i++) {
      cin >> scores[i];
      scores[i]--;
    }
    if (is_sorted(scores.begin(), scores.end())) {
      cout << 0 << endl;
    } else {
      int stage = 0;
      int answer = 1;
      for (int j = 0; j < n; j++) {
        if (scores[j] == j) {
          if (stage == 1) {
            stage = 2;
          }
        } else {
          if (stage == 0) {
            stage = 1;
          } else if (stage == 2) {
            answer = 2;
            break;
          }
        }
      }
      cout << answer << endl;
    }
  }
}
```