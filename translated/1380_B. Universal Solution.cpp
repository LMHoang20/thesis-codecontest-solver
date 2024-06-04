```cpp
#include <iostream>
#include <string>
#include <map>
using namespace std;

int main() {
    map<char, char> winBy = {{'R', 'P'}, {'S', 'R'}, {'P', 'S'}};
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        int maxCnt = 0;
        char maxChar;
        for (char c : s) {
            int cnt = 0;
            for (char d : s) {
                if (c == d) cnt++;
            }
            if (cnt > maxCnt) {
                maxCnt = cnt;
                maxChar = c;
            }
        }
        cout << string(s.size(), winBy[maxChar]) << endl;
    }
    return 0;
}
```