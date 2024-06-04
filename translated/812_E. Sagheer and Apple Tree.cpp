```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXA = 10000000;
vector<int> adjList[100005];
bool blue[100005];
int xorValue, cnt, cntBlue[MAXA + 1], cntRed[MAXA + 1], a[100005];

void dfs(int u)
{
    for (int v : adjList[u])
        dfs(v);
    blue[u] = adjList[u].size() == 0 || !blue[adjList[u][0]];
    if (blue[u])
    {
        xorValue ^= a[u];
        cntBlue[a[u]]++;
        ++cnt;
    }
    else
        cntRed[a[u]]++;
}

int main()
{
    int n;
    cin >> n;
    for (int i = 0; i < n; ++i)
        cin >> a[i];
    for (int i = 1; i < n; ++i)
    {
        int p;
        cin >> p;
        adjList[p - 1].push_back(i);
    }
    dfs(0);
    long long ans = 0;
    if (xorValue == 0)
    {
        for (int i = 1; i <= MAXA; ++i)
            ans += 1ll * cntBlue[i] * cntRed[i];
        long long x = cnt, y = n - x;
        ans += x * (x - 1) / 2 + y * (y - 1) / 2;
    }
    else
    {
        for (int i = 1; i <= MAXA; ++i)
        {
            int j = xorValue ^ i;
            if (j <= MAXA)
                ans += 1ll * cntBlue[i] * cntRed[j];
        }
    }
    cout << ans << endl;
    return 0;
}
```