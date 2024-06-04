#include <bits/stdc++.h>

using namespace std;

int main() {
    int n, p;
    cin >> n >> p;
    int bas = 0;
    vector<int> a(n);
    vector<int> bk(2 * n + 1, 0);
    vector<int> res;
    
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        bas = max(a[i], bas);
    }
    
    for (int i = 0; i < n; i++) {
        bk[max(0, a[i] - bas + n)]++;
    }
    
    for (int i = 1; i <= 2 * n; i++) {
        bk[i] += bk[i - 1];
    }
    
    for (int i = 0; i <= n; i++) {
        bool valid = true;
        for (int j = 0; j < n; j++) {
            if ((bk[i + j] - j) <= 0 || (bk[i + j] - j) % p == 0) {
                valid = false;
                break;
            }
        }
        if (valid) {
            res.push_back(i + (bas - n));
        }
    }
    
    cout << res.size() << endl;
    
    for (int i = 0; i < res.size(); i++) {
        if (i) {
            cout << " ";
        }
        cout << res[i];
    }
    
    cout << endl;
    
    return 0;
}
