```cpp
#include <iostream>

using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, m, k;
        cin >> n >> m >> k;
        cout << (n * m - 1 == k ? "YES" : "NO") << endl;
    }
    return 0;
}
```