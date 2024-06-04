```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<long long> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        long long sum = 0, mx = 0;
        for (int i = 0; i < n; i++) {
            sum += a[i];
            mx = max(mx, a[i]);
        }

        long long k = max(mx, (sum + n - 2) / (n - 1));
        cout << k * (n - 1) - sum << endl;
    }
    return 0;
}
```