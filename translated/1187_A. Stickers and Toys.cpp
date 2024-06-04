```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int tc;
    cin >> tc;
    while (tc--) {
        int n, s, t;
        cin >> n >> s >> t;
        cout << max(n - s, n - t) + 1 << endl;
    }
    return 0;
}
```