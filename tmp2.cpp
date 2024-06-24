// Note: Implementation
#include <bits/stdc++.h>
typedef long double LD;
typedef long long LL;
using namespace std;
const int N = int(1e5 + 3);
int n, m, pos[N];
int main() {
  scanf("%d", &n);
  for (int i = 0; i < n; i++) {
    int num;
    scanf("%d", &num);
    pos[num] = i + 1;
  }
  LL sum1 = 0, sum2 = 0;
  scanf("%d", &m);
  for (int i = 0; i < m; i++) {
    int q;
    scanf("%d", &q);
    sum1 += pos[q];
    sum2 += n - pos[q] + 1;
  }
  printf("%I64d %I64d\n", sum1, sum2);
  return 0;
}
