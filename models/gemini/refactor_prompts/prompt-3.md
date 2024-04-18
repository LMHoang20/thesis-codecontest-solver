## Name

1417_C. k-Amazing Numbers

## Description

You are given an array a consisting of n integers numbered from 1 to n.

Let's define the k-amazing number of the array as the minimum number that occurs in all of the subsegments of the array having length k (recall that a subsegment of a of length k is a contiguous part of a containing exactly k elements). If there is no integer occuring in all subsegments of length k for some value of k, then the k-amazing number is -1.

For each k from 1 to n calculate the k-amazing number of the array a.

Input

The first line contains one integer t (1 ≤ t ≤ 1000) — the number of test cases. Then t test cases follow.

The first line of each test case contains one integer n (1 ≤ n ≤ 3 ⋅ 10^5) — the number of elements in the array. The second line contains n integers a_1, a_2, ..., a_n (1 ≤ a_i ≤ n) — the elements of the array. 

It is guaranteed that the sum of n over all test cases does not exceed 3 ⋅ 10^5.

Output

For each test case print n integers, where the i-th integer is equal to the i-amazing number of the array.

Example

Input


3
5
1 2 3 4 5
5
4 4 4 4 2
6
1 3 1 5 3 1


Output


-1 -1 3 2 1 
-1 4 4 4 2 
-1 -1 1 1 1 1 

## Editorial

Let's fix some arbitrary number $x$ and calculate the minimum value of $k$ such that $x$ occurs in all segments of length $k$. Let $p_1 < p_2 < \dots < p_m$ be the indices of entries of $x$ in the array. Then, for each $1 \le i < m$ it is clear that $k$ should be at least the value of $p_{i+1}-p_i$. Also, $k \ge p_1$ and $k \ge n - p_m + 1$. It is enough to just take the maximum of those values. Let's call this derived value of $k$ as $f(x)$.

Now, we can just go in increasing order of $x$ from $1$ to $n$ and try update the suffix $[f(x), n]$ with $x$. This can be done straightforwardly, just iterating over the range $[f(x), n]$. If we arrive at a cell for which the value of $x$ is already calculated, we immediately terminate our loop and continue our algorithm from $x+1$. 

Time complexity: $O(n)$.

Space complexity: $O(n)$.

## Code

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int, int> pii;
const int MAXN = (int)3e5 + 5;
int f[MAXN], last[MAXN], arr[MAXN], ans[MAXN];
int n;
void solve() {
  scanf("%d", &n);
  for (int i = 1; i <= n; ++i) {
    f[i] = last[i] = 0;
    ans[i] = -1;
  }
  for (int i = 1; i <= n; ++i) {
    scanf("%d", &arr[i]);
  }
  for (int i = 1; i <= n; ++i) {
    int x = arr[i];
    f[x] = max(f[x], i - last[x]);
    last[x] = i;
  }
  for (int x = 1; x <= n; ++x) {
    f[x] = max(f[x], n - last[x] + 1);
    for (int i = f[x]; i <= n && ans[i] == -1; ++i) {
      ans[i] = x;
    }
  }
  for (int i = 1; i <= n; ++i) {
    printf("%d%c", ans[i], " \n"[i == n]);
  }
}
int main() {
  int tt;
  scanf("%d", &tt);
  while (tt--) {
    solve();
  }
  return 0;
}
```

# Answer

Incorrect code:

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int, int> pii;
const int MAXN = (int)3e5 + 5;
int f[MAXN], last[MAXN], ans[MAXN];
int n;

// read the inputs
void read_inputs() {
  scanf("%d", &n);
  for (int i = 1; i <= n; ++i) {
    f[i] = last[i] = 0;
    ans[i] = -1;
  }
  for (int i = 1; i <= n; ++i) {
    scanf("%d", &arr[i]);
  }
}

// initialize the variables
void initialize_vars() {
  for (int i = 1; i <= n; ++i) {
    f[i] = last[i] = 0;
    ans[i] = -1;
  }
}

// find the value of f[x]
void find_f_x(const vector<int>& arr) {
  for (int i = 1; i <= n; ++i) {
    int x = arr[i];
    f[x] = max(f[x], i - last[x]);
    last[x] = i;
  }
  for (int x = 1; x <= n; ++x) {
    f[x] = max(f[x], n - last[x] + 1);
  }
}

// find the answers
void find_answers(const vector<int>& arr) {
  for (int x = 1; x <= n; ++x) {
    for (int i = f[x]; i <= n && ans[i] == -1; ++i) {
      ans[i] = x;
    }
  }
}

// print the output
void print_output() {
  for (int i = 1; i <= n; ++i) {
    printf("%d%c", ans[i], " \n"[i == n]);
  }
}

// solve the problem
void solve(vector<int>& arr) {
  read_inputs();
  initialize_vars();
  find_f_x(arr);
  find_answers(arr);
  print_output();
}

int main() {
  int tt;
  scanf("%d", &tt);
  while (tt--) {
    vector<int> arr(MAXN);
    solve(arr);
  }
  return 0;
}
```

# Compiler Output

tmp.cpp:17:18: error: use of undeclared identifier 'arr'; did you mean 'arg'?
    scanf("%d", &arr[i]);
                 ^~~
                 arg
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/complex:863:1: note: 'arg' declared here
arg(const complex<_Tp>& __c)
^
tmp.cpp:17:18: error: reference to overloaded function could not be resolved; did you mean to call it?
    scanf("%d", &arr[i]);
                 ^~~
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/complex:863:1: note: possible target for call
arg(const complex<_Tp>& __c)

# Answer

Correct code:

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int, int> pii;
const int MAXN = (int)3e5 + 5;
int f[MAXN], last[MAXN], ans[MAXN];
vector<int> arr(MAXN);
int n;

// read the inputs
void read_inputs() {
  scanf("%d", &n);
  for (int i = 1; i <= n; ++i) {
    f[i] = last[i] = 0;
    ans[i] = -1;
  }
  for (int i = 1; i <= n; ++i) {
    scanf("%d", &arr[i]);
  }
}

// initialize the variables
void initialize_vars() {
  for (int i = 1; i <= n; ++i) {
    f[i] = last[i] = 0;
    ans[i] = -1;
  }
}

// find the value of f[x]
void find_f_x() {
  for (int i = 1; i <= n; ++i) {
    int x = arr[i];
    f[x] = max(f[x], i - last[x]);
    last[x] = i;
  }
  for (int x = 1; x <= n; ++x) {
    f[x] = max(f[x], n - last[x] + 1);
  }
}

// find the answers
void find_answers() {
  for (int x = 1; x <= n; ++x) {
    for (int i = f[x]; i <= n && ans[i] == -1; ++i) {
      ans[i] = x;
    }
  }
}

// print the output
void print_output() {
  for (int i = 1; i <= n; ++i) {
    printf("%d%c", ans[i], " \n"[i == n]);
  }
}

// solve the problem
void solve() {
  read_inputs();
  initialize_vars();
  find_f_x();
  find_answers();
  print_output();
}

int main() {
  int tt;
  scanf("%d", &tt);
  while (tt--) {
    solve();
  }
  return 0;
}
```

# Compiler Output

OK
