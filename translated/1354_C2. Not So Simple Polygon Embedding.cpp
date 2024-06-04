```cpp
#include <bits/stdc++.h>
using namespace std;
const double PI = acos(-1.0);
int main() {
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        double ans;
        if (n % 2 == 0) {
            ans = 1.0 / tan(PI / (2 * n));
        } else {
            ans = cos(PI / (4 * n)) / sin(PI / (2 * n));
        }
        cout << fixed << setprecision(9) << ans << endl;
    }
    return 0;
}
```