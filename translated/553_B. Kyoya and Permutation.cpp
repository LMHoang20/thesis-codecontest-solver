#include <bits/stdc++.h>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int N;
    long long K;
    cin >> N >> K;
    
    vector<long long> fib(N + 1);
    fib[0] = fib[1] = 1;
    for (int i = 2; i <= N; ++i) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    
    int idx = 0;
    vector<int> res(N);
    while (idx < N) {
        if (K <= fib[N - idx - 1]) {
            res[idx] = idx + 1;
            ++idx;
        } else {
            K -= fib[N - idx - 1];
            res[idx] = idx + 2;
            res[idx + 1] = idx + 1;
            idx += 2;
        }
    }
    
    for (int i = 0; i < N; ++i) {
        cout << res[i] << " ";
    }
    cout << endl;
    
    return 0;
}
