```cpp
#include <iostream>
#include <vector>
using namespace std;

long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}

long long phi(long long a) {
    long long tmp = a, ans = a;
    long long d = 2;
    while (d * d <= tmp) {
        long long cnt = 0;
        while (tmp % d == 0) {
            tmp /= d;
            cnt++;
        }
        if (cnt > 0) ans -= ans / d;
        d++;
    }
    if (tmp > 1) ans -= ans / tmp;
    return ans;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, m;
        cin >> a >> m;
        cout << phi(m / gcd(a, m)) << endl;
    }
    return 0;
}
```