```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, k;
        cin >> n >> k;
        vector<int> h(n);
        for (int i = 0; i < n; i++) {
            cin >> h[i];
        }

        bool ok = true;
        int mn = h[0], mx = h[0];
        for (int i = 1; i < n; i++) {
            mn = max(mn - k + 1, h[i]);
            mx = min(mx + k - 1, h[i] + k - 1);
            if (mn > mx) {
                ok = false;
                break;
            }
        }
        if (h[n - 1] < mn || h[n - 1] > mx)
            ok = false;
        cout << (ok ? "YES" : "NO") << endl;
    }
    return 0;
}
```