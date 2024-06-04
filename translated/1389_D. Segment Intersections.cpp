```cpp
#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < (n); ++i)
#define repA(i, a, n) for (int i = a; i <= (n); ++i)
#define repD(i, a, n) for (int i = a; i >= (n); --i)
#define trav(a, x) for (auto &a : x)
#define all(x) x.begin(), x.end()
#define sz(x) (int)x.size()
#define fill(a) memset(a, 0, sizeof(a))
#define fst first
#define snd second
#define mp make_pair
#define pb push_back
#define eb emplace_back

typedef long long ll;
typedef long double ld;
typedef pair<ll, ll> pl;
typedef vector<int> vi;
typedef vector<ll> vl;
typedef vector<bool> vb;
typedef vector<string> vs;

const double PI = acos(-1);
const ll mod = 1e9 + 7;
const int inf = 1e9 + 7;
const ll linf = 1e18 + 7;
const int N = 2e5 + 7;
const int maxN = 1e6 + 7;

ll n, k;
ll l1, r1, l2, r2;

ll solve() {
  ll ans = 1e18;
  if (max(l1, l2) <= min(r1, r2)) {
    ll rem = max(0ll, k - n * (min(r1, r2) - max(l1, l2)));
    ll maxPossible = n * (abs(l1 - l2) + abs(r1 - r2));
    ans = min(rem, maxPossible) + max(0ll, rem - maxPossible) * 2;
  } else {
    ll invest = max(l1, l2) - min(r1, r2);
    repA(cntInv, 1, n) {
      ll curAns = invest * cntInv;
      ll maxPossible = (max(r1, r2) - min(l1, l2)) * cntInv;
      curAns += min(k, maxPossible) + max(0ll, k - maxPossible) * 2;
      ans = min(ans, curAns);
    }
  }
  return ans;
}

int main() {
  cin.tie(0);
  cout.tie(0);
  cin.sync_with_stdio(0);

  int t;
  cin >> t;
  while (t--) {
    cin >> n >> k;
    cin >> l1 >> r1;
    cin >> l2 >> r2;
    cout << solve() << '\n';
  }

  return 0;
}
```