#include <bits/stdc++.h>
using namespace std;
int main() {
    int T;
    cin >> T;
    while (T--) {
        string t;
        cin >> t;
        bool has_one = false, has_zero = false;
        bool start_with_one = t[0] == '1';
        for (int i = 0; i < t.size(); i++) {
            if (t[i] == '1') {
                has_one = true;
            } else {
                has_zero = true;
            }
        }
        if (has_one && !has_zero) {
            cout << string(2 * t.size(), '1') << endl;
        } else if (has_zero && !has_one) {
            cout << string(2 * t.size(), '0') << endl;
        } else {
            int d = start_with_one;
            for (int i = 0; i < t.size(); i++) {
                cout << d << 1 - d;
            }
            cout << endl;
        }
    }
}