```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const int MOD = 998244353;

int mul(int a, int b) {
    return (int)((long long)a * (long long)b % MOD);
}

int f[500042];
int rf[500042];

int C(int n, int k) {
    return (k < 0 || k > n) ? 0 : mul(f[n], mul(rf[n - k], rf[k]));
}

int pow(int a, int n) {
    int res = 1;
    while (n != 0) {
        if ((n & 1) == 1) {
            res = mul(res, a);
        }
        a = mul(a, a);
        n >>= 1;
    }
    return res;
}

static void shuffleArray(int *a, int n) {
    random_device rd;
    mt19937 g(rd());
    for (int i = n - 1; i > 0; i--) {
        int index = g() % (i + 1);
        int tmp = a[index];
        a[index] = a[i];
        a[i] = tmp;
    }
}

int inv(int a) {
    return pow(a, MOD - 2);
}

void doIt() {
    int n, k;
    cin >> n >> k;

    f[0] = rf[0] = 1;
    for (int i = 1; i < 500042; ++i) {
        f[i] = mul(f[i - 1], i);
        rf[i] = mul(rf[i - 1], inv(i));
    }

    int events[2 * n];
    for (int i = 0; i < n; ++i) {
        int le, ri;
        cin >> le >> ri;
        events[i] = le * 2;
        events[i + n] = ri * 2 + 1;
    }
    shuffleArray(events, 2 * n);
    sort(events, events + 2 * n);

    int ans = 0;
    int balance = 0;
    for (int r = 0; r < 2 * n;) {
        int l = r;
        while (r < 2 * n && events[l] == events[r]) {
            ++r;
        }
        int added = r - l;
        if (events[l] % 2 == 0) {
            // Open event
            ans += C(balance + added, k);
            if (ans >= MOD) ans -= MOD;
            ans += MOD - C(balance, k);
            if (ans >= MOD) ans -= MOD;
            balance += added;
        } else {
            // Close event
            balance -= added;
        }
    }

    cout << ans << endl;
}

int main() {
    doIt();
    return 0;
}
```