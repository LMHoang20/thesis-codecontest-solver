```cpp
#include <bits/stdc++.h>

using namespace std;

const int MAXN = 1e5 + 5;

struct point {
  int x, y;
  point() {}
  point(int x, int y) : x(x), y(y) {}
};

int n;
point pts[MAXN];
int szAns;

bool cmp(const point &a, const point &b) {
  int dist1 = abs(a.x) + abs(a.y);
  int dist2 = abs(b.x) + abs(b.y);

  return dist1 < dist2;
}

int main() {
  cin >> n;
  for (int i = 0; i < n; i++) {
    int x, y;
    cin >> x >> y;
    szAns += 2;
    if (x != 0) szAns += 2;
    if (y != 0) szAns += 2;
    pts[i] = point(x, y);
  }

  sort(pts, pts + n, cmp);
  cout << szAns << endl;
  for (int i = 0; i < n; i++) {
    if (pts[i].x > 0) cout << "1 " << pts[i].x << " R" << endl;
    if (pts[i].x < 0) cout << "1 " << -pts[i].x << " L" << endl;
    if (pts[i].y > 0) cout << "1 " << pts[i].y << " U" << endl;
    if (pts[i].y < 0) cout << "1 " << -pts[i].y << " D" << endl;
    cout << "2" << endl;
    if (pts[i].x > 0) cout << "1 " << pts[i].x << " L" << endl;
    if (pts[i].x < 0) cout << "1 " << -pts[i].x << " R" << endl;
    if (pts[i].y > 0) cout << "1 " << pts[i].y << " D" << endl;
    if (pts[i].y < 0) cout << "1 " << -pts[i].y << " U" << endl;
    cout << "3" << endl;
  }

  return 0;
}
```