```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
    int q;
    cin >> q;
    while (q--) {
        int n;
        cin >> n;
        int odd = 0, evenGood = 0, evenBad = 0;
        for (int i = 0; i < n; i++) {
            string s;
            cin >> s;
            if (s.length() % 2 == 1)
                odd++;
            else if (count(s.begin(), s.end(), '0') % 2 == 0)
                evenGood++;
            else
                evenBad++;
        }
        cout << n - (odd == 0 && evenBad % 2 == 1 ? 1 : 0) << endl;
    }
    return 0;
}
```