
#include <bits/stdc++.h>

using namespace std;

const int MAX_N = 2e5 + 5;

int n;
int a[MAX_N];
int f[MAX_N];
int cnt[MAX_N];

int main() {
    cin >> n;

    int q = 0;
    int distinct = 0;

    for (int i = 1; i <= n; i++) {
        if (i == 1 || a[i] != a[i - 1]) {
            distinct++;
            f[distinct] = 1;
            cnt[distinct] = i;
            a[distinct] = a[i];
        } else {
            f[distinct]++;
        }
    }

    int l = 1, r = distinct;
    while (l <= r) {
        int mid = (l + r) / 2;
        cout << "? " << cnt[mid] << " " << cnt[mid] + f[mid] - 1 << endl;
        cout.flush();
        int x, y;
        cin >> x >> y;
        q++;
        if (x != a[mid]) {
            r = mid - 1;
        } else {
            l = mid + 1;
        }
    }

    cout << "! ";
    for (int i = 1; i <= distinct; i++) {
        for (int j = 0; j < f[i]; j++) {
            cout << a[i] << " ";
        }
    }
    cout << endl;

    return 0;
}

