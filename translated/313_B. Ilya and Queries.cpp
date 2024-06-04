```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    string s;
    int n, m;
    cin >> s;
    n = s.size();
    vector<int> a(n + 1, 0);
    for (int i = 1; i < n; i++) {
        if (s[i] == s[i - 1]) a[i] = 1;
    }
    vector<int> sum(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        sum[i] = sum[i - 1] + a[i];
    }
    cin >> m;
    vector<pair<int, int>> queries(m);
    for (int i = 0; i < m; i++) {
        cin >> queries[i].first >> queries[i].second;
    }
    for (int i = 0; i < m; i++) {
        cout << sum[queries[i].second - 1] - sum[queries[i].first - 1] << endl;
    }
    return 0;
}
```