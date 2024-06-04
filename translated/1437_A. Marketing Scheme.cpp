```cpp
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long l, r;
        cin >> l >> r;
        cout << (2 * l > r ? "YES" : "NO") << endl;
    }
    return 0;
}
```