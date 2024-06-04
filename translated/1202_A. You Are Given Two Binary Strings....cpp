```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
    int T;
    cin >> T;
    for (int tc = 1; tc <= T; tc++) {
        string x, y;
        cin >> x >> y;
        reverse(x.begin(), x.end());
        reverse(y.begin(), y.end());
        int posY = y.find('1');
        int posX = x.find('1', posY);
        cout << posX - posY << endl;
    }
    return 0;
}
```