```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const int MAXN = 3e5 + 10;

ll a[MAXN];
int n, lf, rg;
ll tg[MAXN][20];
ll tm[MAXN][20];

int gcd(ll a, ll b) {
  if (a == 0)
    return b;
  return gcd(b % a, a);
}

int main() {
  cin >> n;
  for (int i = 0; i < n; i++) cin >> a[i];

  lf = 1;
  rg = n + 1;

  for (int j = 0; j < 20; j++) {
    if (j == 0) {
      for (int i = 0; i < n; i++) {
        tm[i][j] = a[i];
        tg[i][j] = a[i];
      }
      continue;
    }

    for (int i = 0; i < n; i++) {
      if (tg[i][j - 1] == -1) continue;
      int tv = i + (1 << (j - 1));
      if (tv >= n) continue;
      if (tg[tv][j - 1] == -1) continue;
      tg[i][j] = gcd(tg[i][j - 1], tg[tv][j - 1]);
      tm[i][j] = min(tm[i][j - 1], tm[tv][j - 1]);
    }
  }

  while (rg - lf > 1) {
    int mid = (lf + rg) >> 1;

    bool ok = false;

    int power = 0;

    while ((1 << power) <= mid) power++;
    power--;

    for (int i = 0; (i <= n - mid) && !ok; i++) {
      int g = tg[i][power];
      int b = i + mid - 1;
      g = gcd(tg[b - (1 << power) + 1][power], g);
      g -= min(tm[i][power], tm[b - (1 << power) + 1][power]);

      if (g == 0) ok = true;
    }

    if (ok)
      lf = mid;
    else
      rg = mid;
  }
  int power = 0;

  while ((1 << power) <= lf) power++;
  power--;

  int anscnt = 0;
  for (int i = 0; (i <= n - lf); i++) {
    int g = tg[i][power];
    int b = i + lf - 1;
    g = gcd(tg[b - (1 << power) + 1][power], g);
    g -= min(tm[i][power], tm[b - (1 << power) + 1][power]);

    if (g == 0) { anscnt++; }
  }
  cout << anscnt << " " << (lf - 1) << endl;
  for (int i = 0; (i <= n - lf); i++) {
    int g = tg[i][power];
    int b = i + lf - 1;
    g = gcd(tg[b - (1 << power) + 1][power], g);
    g -= min(tm[i][power], tm[b - (1 << power) + 1][power]);

    if (g == 0) { cout << i + 1 << " "; }
  }

  return 0;
}
```