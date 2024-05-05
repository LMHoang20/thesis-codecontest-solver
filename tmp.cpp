#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
template <typename T> bool chkmax(T &x, T y) { return x < y ? x = y, true : false; }
template <typename T> bool chkmin(T &x, T y) { return x > y ? x = y, true : false; }
int readint() {
  int x = 0, f = 1;
  char ch = getchar();
  while (ch < '0' || ch > '9') {
    if (ch == '-') {
      f = -1;
    }
    ch = getchar();
  }
  while (ch >= '0' && ch <= '9') {
    x = x * 10 + ch - '0';
    ch = getchar();
  }
  return x * f;
}
const int cys = 998244353;
int n;
ll fac[5005], inv[5005], d[5005][5005], ans[5005];
ll qpow(ll x, ll p) {
  ll ret = 1;
  for (; p; p >>= 1, x = x * x % cys) {
    if (p & 1) {
      ret = ret * x % cys;
    }
  }
  return ret;
}
int main() {
  n = readint();
  d[0][0] = fac[0] = inv[0] = 1;
  for (int i = 1; i <= n; i++) {
    fac[i] = fac[i - 1] * i % cys;
  }
  inv[n] = qpow(fac[n], cys - 2);
  for (int i = n - 1; i >= 1; i--) {
    inv[i] = inv[i + 1] * (i + 1) % cys;
  }
  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
      d[i][j] = (d[i - 1][j - 1] * (i - j + 1) + d[i - 1][j] * j) % cys;
    }
  }
  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
      ans[i] = (ans[i] + d[j][i] * inv[j]) % cys;
    }
  }
  for (int i = 1; i <= n; i++) {
    printf("%lld ", ans[i] * fac[n] % cys);
  }
  printf("\n");
  return 0;
}
