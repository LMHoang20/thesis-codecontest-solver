```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

const string dirs = "NSEW";

int main() {
    int n;
    cin >> n;
    --n;
    string s1, s2;
    cin >> s1 >> s2;
    string sb;
    for (int i = 0; i < n; ++i) {
        sb += dirs[dirs.find(s1[n - i - 1]) ^ 1];
    }
    sb += s2;
    vector<int> p(2 * n);
    for (int i = 1; i < 2 * n; ++i) {
        p[i] = p[i - 1];
        while (p[i] != 0 && sb[i] != sb[p[i]]) {
            p[i] = p[p[i] - 1];
        }
        if (sb[i] == sb[p[i]]) {
            p[i]++;
        }
    }
    cout << (p[2 * n - 1] == 0 ? "YES" : "NO") << endl;
    return 0;
}
```