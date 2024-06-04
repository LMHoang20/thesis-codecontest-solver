```cpp
#include <iostream>
#include <algorithm>

using namespace std;

int main() {
    int q;
    cin >> q;
    for (int ct = 1; ct <= q; ct++) {
        int n, x, a, b;
        cin >> n >> x >> a >> b;
        cout << min(n - 1, abs(a - b) + x) << endl;
    }
    return 0;
}
```