```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int T;
    cin >> T;
    for (int tc = 1; tc <= T; tc++) {
        int n, x;
        cin >> n >> x;
        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }
        sort(a.rbegin(), a.rend());

        int cnt = 0;
        long long sum = 0;
        while (cnt < n && sum + a[cnt] >= (cnt + 1) * x) {
            sum += a[cnt];
            cnt++;
        }
        cout << cnt << endl;
    }
    return 0;
}
```