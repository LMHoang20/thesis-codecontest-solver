```cpp
#include <bits/stdc++.h>
using namespace std;
const int maxn = 2e5 + 5;
const long long inf = 86603878;
int n;
long long a[maxn];

int main() {
    cin >> n;
    int m = (n + 1) / 2;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }
    long long curr = 0;
    for (int j = 0; j < m; j++) {
        curr += a[2 * j + 1];
    }
    long long answer = curr;
    for (int j = 0; j < n - 1; j++) {
        curr -= a[(2 * j) % n + 1];
        curr += a[(2 * (j + m)) % n + 1];
        answer = max(answer, curr);
    }
    cout << answer << endl;
}
```