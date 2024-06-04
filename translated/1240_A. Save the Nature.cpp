```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
    int q;
    cin >> q;
    while (q--) {
        int n;
        cin >> n;
        vector<int> p(n);
        for (int i = 0; i < n; i++) {
            cin >> p[i];
            p[i] /= 100;
        }
        int x, a, y, b;
        cin >> x >> a >> y >> b;
        ll k;
        cin >> k;
        if (x < y) {
            swap(x, y);
            swap(a, b);
        }
        sort(p.begin(), p.end(), greater<int>());
        int l = 0, r = n + 1;
        while (r - l > 1) {
            int mid = (l + r) / 2;
            ll sum = 0;
            int cXY = 0, cX = 0, cY = 0;
            for (int i = 1; i <= mid; i++) {
                if (i % a == 0 && i % b == 0)
                    cXY++;
                else if (i % a == 0)
                    cX++;
                else if (i % b == 0)
                    cY++;
            }
            for (int i = 0; i < cXY; i++) sum += p[i] * (x + y);
            for (int i = 0; i < cX; i++) sum += p[cXY + i] * x;
            for (int i = 0; i < cY; i++) sum += p[cXY + cX + i] * y;
            if (sum >= k)
                r = mid;
            else
                l = mid;
        }
        if (r > n) r = -1;
        cout << r << endl;
    }
    return 0;
}
```