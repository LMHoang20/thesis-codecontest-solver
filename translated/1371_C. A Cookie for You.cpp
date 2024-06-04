#include<stdio.h>
 
int main(){
    int t;
    cin >> t;
    while (t--) {
        long long n, r;
        cin >> n >> r;
        long long l = 1, res = 0;
        if (n <= l) {
            cout << 1 << endl;
            continue;
        }
        if (n <= r) {
            r = n - 1;
            res = 1;
        }
        cout << res + ((l + r) * (r - l + 1)) / 2 << endl;
    }
    return 0;
}