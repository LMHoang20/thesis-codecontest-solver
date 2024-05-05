#include <bits/stdc++.h>
using namespace std;
template <class T>
void debug(T a, T b) {
  ;
}
template <class T>
void chmin(T& a, const T& b) {
  if (a > b) a = b;
}
template <class T>
void chmax(T& a, const T& b) {
  if (a < b) a = b;
}
namespace std {
template <class S, class T>
ostream& operator<<(ostream& out, const pair<S, T>& a) {
  out << '(' << a.first << ',' << a.second << ')';
  return out;
}
}  // namespace std
long long int readL() {
  long long int res;
  scanf("%I64d", &res);
  return res;
}
void printL(long long int res) { printf("%I64d", res); }
const long long int INF = 1e18;
int n, k;
set<pair<long long int, pair<int, int> > > inter;
set<int> exist;
long long int ar[100005];
int main() {
  cin >> n >> k;
  k += 2;
  int m = 0;
  ar[0] = INF;
  ar[1] = 2 * INF;
  for (int i = 0; i < (n); ++i) {
    ar[i + 2] = readL();
  }
  ar[n + 2] = -INF;
  ar[n + 3] = 0;
  n += 4;
  long long int res = 0;
  for (int i = 0; i < (n); ++i) {
    int j = i;
    while (j + 1 < n && ar[j + 1] <= ar[j]) {
      ++j;
    }
    int k = j + 1;
    while (k + 1 < n && ar[k + 1] >= ar[k]) ++k;
    if (k < n) {
      res += ar[k] - ar[j];
      ar[m++] = ar[j];
      ar[m++] = ar[k];
    }
    i = k;
  }
  for (int i = 0; i < (m); ++i) exist.insert(i);
  n = m;
  for (int i = 0; i < (m / 2); ++i)
    inter.insert(make_pair(ar[i * 2 + 1] - ar[i * 2], make_pair(i * 2, 0)));
  for (int i = 0; i < (m / 2 - 1); ++i)
    inter.insert(
        make_pair(ar[i * 2 + 1] - ar[i * 2 + 2], make_pair(i * 2 + 1, 1)));
  for (int hoge = 0; hoge < (m / 2 - k); ++hoge) {
    auto it = inter.begin();
    res -= it->first;
    if (it->second.second == 0) {
      int pos = it->second.first;
      auto p1 = exist.find(pos);
      ;
      ;
      auto p2 = p1;
      ++p2;
      auto q2 = p1;
      --q2;
      auto q1 = q2;
      --q1;
      auto r1 = p2;
      ++r1;
      auto r2 = r1;
      ++r2;
      inter.erase(inter.begin());
      inter.erase(make_pair(-(ar[*p1] - ar[*q2]), make_pair(*q2, 1)));
      inter.erase(make_pair(-(ar[*r1] - ar[*p2]), make_pair(*p2, 1)));
      inter.insert(make_pair(-(ar[*r1] - ar[*q2]), make_pair(*q2, 1)));
      exist.erase(p2);
      exist.erase(pos);
    } else {
      int pos = it->second.first;
      auto p2 = exist.find(pos);
      auto p1 = p2;
      --p1;
      inter.erase(inter.begin());
      inter.erase(make_pair(ar[*p2] - ar[*p1], make_pair(*p1, 0)));
      auto q1 = p2;
      ++q1;
      auto q2 = q1;
      ++q2;
      inter.erase(make_pair(ar[*q2] - ar[*q1], make_pair(*q1, 0)));
      inter.insert(make_pair(ar[*q2] - ar[*p1], make_pair(*p1, 0)));
      exist.erase(p2);
      q1 = exist.lower_bound(pos);
      exist.erase(q1);
    }
  }
  res -= 2 * INF;
  cout << res << endl;
  return 0;
}
