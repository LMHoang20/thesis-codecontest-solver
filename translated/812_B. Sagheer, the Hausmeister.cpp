```cpp
#include <bits/stdc++.h>
using namespace std;

const int maxn = 15, maxm = 100;
int n, m;
string a[maxn];
int leftMost[maxn], rightMost[maxn];
int maxFloor = -1;

int main() {
    cin >> n >> m;
    memset(leftMost, 0x3f, sizeof leftMost);
    for (int i = n - 1; i >= 0; --i) {
        cin >> a[i];
        for (int j = 0; j < m + 2; ++j)
            if (a[i][j] == '1') {
                rightMost[i] = j;
                if (maxFloor == -1) maxFloor = i;
            }
        for (int j = m + 1; j >= 0; --j)
            if (a[i][j] == '1') leftMost[i] = j;
    }

    int ans = 1e9;
    for (int stairs = 0; stairs < (1 << n - 1); ++stairs) {
        int cur = 0, room = 0, floor = 0;
        while (floor <= maxFloor) {
            if (room == 0) {
                cur += rightMost[floor] - room;
                room = rightMost[floor];
            } else {
                cur += room - leftMost[floor];
                room = leftMost[floor];
            }
            if (floor == maxFloor) break;
            int nxtStairs = (stairs & (1 << floor)) == 0 ? 0 : m + 1;
            cur += abs(nxtStairs - room) + 1;
            room = nxtStairs;
            ++floor;
        }
        ans = min(ans, cur);
    }
    cout << ans << '\n';
    return 0;
}
```