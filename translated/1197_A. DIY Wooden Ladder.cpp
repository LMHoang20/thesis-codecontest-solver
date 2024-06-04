```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; i++) { cin >> a[i]; }
        sort(a.rbegin(), a.rend());
        cout << min(a[1] - 1, n - 2) << endl;
    }
    return 0;
}
```