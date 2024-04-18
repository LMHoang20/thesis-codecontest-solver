<TARGET>
problem name: Maximize the Remaining String
</TARGET>
<EDITORIAL>
[1506A - Strange Table](/contest/1506/problem/A)

Problem author: [sodafago](/profile/sodafago)

 **Editorial** 
### [1506A - Strange Table](/contest/1506/problem/A)

To find the cell number in a different numbering, you can find $ (r,c)$ (latex: $(r, c)$) coordinates of the cell with the number $ x$ (latex: $x$) in the numbering **"by columns"**: 

 -  $ r=((x-1)\phantom{\rule{0.667em}{0ex}}\mathrm{mod}\phantom{\rule{0.16666666666666666em}{0ex}}\phantom{\rule{0.16666666666666666em}{0ex}}r)+1$ (latex: $r = ((x-1) \mod r) + 1$), where $ a\phantom{\rule{0.667em}{0ex}}\mathrm{mod}\phantom{\rule{0.16666666666666666em}{0ex}}\phantom{\rule{0.16666666666666666em}{0ex}}b$ (latex: $a \mod b$) is the remainder of dividing the number $ a$ (latex: $a$) by the number $ b$ (latex: $b$); 
-  $ c=\lceil \frac{x}{n}\rceil $ (latex: $c = \left\lceil \frac{x}{n} \right\rceil$), where $ \lceil \frac{a}{b}\rceil $ (latex: $\left\lceil \frac{a}{b} \right\rceil$) is the division of the number $ a$ (latex: $a$) to the number $ b$ (latex: $b$) rounded up. 
Then, the cell number in numbering **"by lines"** will be equal to $ (r-1)\ast m+c$ (latex: $(r-1)*m + c$).

 **Solution** 
```
#include <bits/stdc++.h>

using namespace std;
using ll = long long;

void solve() {
    ll n, m, x;
    cin >> n >> m >> x;
    x--;
    ll col = x / n;
    ll row = x % n;
    cout << row * m + col + 1 << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr); cout.tie(nullptr);
    int n;
    cin >> n;
    while (n--) {
        solve();
    }
}
```

[1506B - Partial Replacement](/contest/1506/problem/B)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506B - Partial Replacement](/contest/1506/problem/B)

To solve this problem, you can use the dynamic programming method or the greedy algorithm. Let's describe the greedy solution.

Until we get to the last character '`*`' we will do the following: 

 -  being in position $ i$ (latex: $i$), find the maximum $ j$ (latex: $j$), such that $ {s}_{j}=$ (latex: $s_j=$)'`*`' and $ j-i\le k$ (latex: $j-i \le k$), and move to position $ j$ (latex: $j$). 
Since we make the longest move on each turn, we will make the minimum number of substitutions.

 **Solution** 
```
#include <bits/stdc++.h>
using namespace std;

void solve() {
  int n, k;
  cin >> n >> k;
  string s;
  cin >> s;
  int res = 1;
  int i = s.find_first_of('*');
  while (true) {
    int j = min(n - 1, i + k);
    for (; i < j && s[j] == '.'; j--) {}
    if (i == j) {
      break;
    }
    res++;
    i = j;
  }
  cout << res << "\n";
}

int main() {
  int tests;
  cin >> tests;
  while (tests-- > 0) {
    solve();
  }
  return 0;
}
```

[1506C - Double-ended Strings](/contest/1506/problem/C)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506C - Double-ended Strings](/contest/1506/problem/C)

Regarding to the small constraints, in this problem you could iterate over how many characters were removed by each type of operation. If $ l$ (latex: $l$) characters at the beginning and $ x$ (latex: $x$) characters at the end are removed from the string $ s$ (latex: $s$), then the substring $ s[l+1,n-x]$ (latex: $s[l+1, n-x]$) remains, where $ n$ (latex: $n$) — is the length of the string $ s$ (latex: $s$).

There is also a fast solution to this problem using dynamic programming.

 **Solution** 
```
#include <bits/stdc++.h>

using namespace std;
using ll = long long;

void solve() {
    string a, b;
    cin >> a >> b;
    int n = a.size(), m = b.size();
    int ans = 0;
    for (int len = 1; len <= min(n, m); len++) {
        for (int i = 0; i + len <= n; i++) {
            for (int j = 0; j + len <= m; j++) {
                if (a.substr(i, len) == b.substr(j, len)) {
                    ans = max(ans, len);
                }
            }
        }
    }
    cout << a.size() + b.size() - 2 * ans << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr); cout.tie(nullptr);
    int n;
    cin >> n;
    while (n--) {
        solve();
    }
}
```

[1506D - Epic Transformation](/contest/1506/problem/D)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506D - Epic Transformation](/contest/1506/problem/D)

Let's replace each character with the number of its occurrences in the string. Then each operation — take two non-zero numbers and subtract one from them. In the end, we will have only one non-zero number left, and we want to minimize it. We can say that we want to minimize the maximum number after applying all the operations, which means we want to minimize the maximum number at each step.

We get the following greedy solution — each time we take two characters with maximal occurrences number and delete them.

 **Solution** 
```
#include <bits/stdc++.h>

using namespace std;
using ll = long long;

void solve() {
    priority_queue<pair<int, int>> q;
    int n;
    cin >> n;
    map<int, int> v;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        v[x]++;
    }
    for (auto [x, y] : v) {
        q.push({y, x});
    }
    int sz = n;
    while (q.size() >= 2) {
        auto [cnt1, x1] = q.top();
        q.pop();
        auto [cnt2, x2] = q.top();
        q.pop();
        cnt1--;
        cnt2--;
        sz -= 2;
        if (cnt1) {
            q.push({cnt1, x1});
        }
        if (cnt2) {
            q.push({cnt2, x2});
        }
    }
    cout << sz << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr); cout.tie(nullptr);
    int n;
    cin >> n;
    while (n--) {
        solve();
    }
}
```

[1506E - Restoring the Permutation](/contest/1506/problem/E)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506E - Restoring the Permutation](/contest/1506/problem/E)

If we want to build a minimal lexicographic permutation, we need to build it from left to right by adding the smallest possible element. If $ q[i]=q[i-1]$ (latex: $q[i] = q[i-1]$), so the new number must not be greater than all the previous ones, and if $ q[i]>q[i-1]$ (latex: $q[i] > q[i-1]$), then necessarily $ a[i]=q[i]$ (latex: $a[i] = q[i]$). $ q[i]<q[i-1]$ (latex: $q[i] < q[i-1]$) does not happen, since $ q[i]$ (latex: $q[i]$) — is the maximum element among the first $ i$ (latex: $i$) elements.

We get a greedy solution if $ q[i]>q[i-1]$ (latex: $q[i] > q[i-1]$), then $ a[i]=q[i]$ (latex: $a[i] = q[i]$), otherwise we put the minimum character that has not yet occurred in the permutation.

 **Solution** 
```
#include <bits/stdc++.h>
using namespace std;

void placeLeft(vector<int> &q, bool minimize) {
  set<int> left;
  for (int i = 1; i <= (int) q.size(); i++) {
    left.insert(i);
  }
  for (int i : q) {
    if (i != -1) {
      left.erase(i);
    }
  }
  int lastPlaced = -1;
  for (int &i : q) {
    if (i == -1) {
      set<int>::const_iterator it;
      if (minimize) {
        it = left.begin();
      } else {
        it = --left.lower_bound(lastPlaced);
      }
      i = *it;
      left.erase(it);
    } else {
      lastPlaced = i;
    }
  }
}

void solve() {
  int n;
  cin >> n;
  vector<int> q(n);
  for (int i = 0; i < n; i++) {
    cin >> q[i];
  }

  vector<int> res1(n, -1), res2(n, -1);
  for (int i = 0, lastPlaced = -1; i < n; lastPlaced = q[i], i++) {
    if (lastPlaced != q[i]) {
      res1[i] = q[i];
      res2[i] = q[i];
    }
  }
  placeLeft(res1, true);
  placeLeft(res2, false);
  for (int x : res1) {
    cout << x << " ";
  }
  cout << "\n";
  for (int x : res2) {
    cout << x << " ";
  }
  cout << "\n";
}

int main() {
  int tests;
  cin >> tests;
  while (tests-- > 0) {
    solve();
  }
  return 0;
}
```

[1506F - Triangular Paths](/contest/1506/problem/F)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov), [Stepavly](/profile/Stepavly), [Supermagzzz](/profile/Supermagzzz)

 **Editorial** 
### [1506F - Triangular Paths](/contest/1506/problem/F)

Since all edges are directed downward, there is only one way to visit all $ n$ (latex: $n$) points is to visit the points in ascending order of the layer number. Let's sort the points in order of increasing layer.

It is easy to see that the cost of the entire path is equal to the sum of the cost of paths between adjacent points. Let's learn how to calculate the cost of a path between two points $ ({r}_{1},{c}_{1})$ (latex: $(r_1, c_1)$) and $ ({r}_{2},{c}_{2})$ (latex: $(r_2, c_2)$): 

 -  If $ {r}_{1}-{c}_{1}={r}_{2}-{c}_{2}$ (latex: $r_1 - c_1 = r_2 - c_2$), then if $ ({r}_{1}+{c}_{1})$ (latex: $(r_1 + c_1)$) is even, then the cost is $ {r}_{2}-{r}_{1}$ (latex: $r_2-r_1$), otherwise the cost is $ 0$ (latex: $0$); 
-  Otherwise, move the point $ ({r}_{2},{c}_{2})$ (latex: $(r_2, c_2)$) to $ ({r}_{3},{c}_{3})=({r}_{2}-{r}_{1}+1,{c}_{2}-{c}_{1}+1)$ (latex: $(r_3, c_3) = (r_2-r_1+1, c_2-c_1+1)$) and find the cost of the path $ (1,1)\to ({r}_{3},{c}_{3})$ (latex: $(1, 1) \rightarrow (r_3, c_3)$) with different criteria for the activation of the edges; 
-  If $ ({r}_{1}+{c}_{1})$ (latex: $(r_1 + c_1)$) is even then the cost is $ \lfloor \frac{{r}_{3}-{c}_{3}}{2}\rfloor $ (latex: $\lfloor \frac{r_3-c_3}{2} \rfloor$); 
-  Otherwise, the cost is $ \lceil \frac{{r}_{3}-{c}_{3}}{2}\rceil $ (latex: $\lceil \frac{r_3-c_3}{2} \rceil$); 

 **Solution** 
```
#include <bits/stdc++.h>
using namespace std;

bool isLeftArrow(int r, int c) {
  return (r + c) % 2 == 0;
}

bool isRightArrow(int r, int c) {
  return (r + c) % 2 == 1;
}

int calcDist(int r1, int c1, int r2, int c2) {
  if (r1 - c1 == r2 - c2) {
    return isRightArrow(r1, c1) ? 0 : r2 - r1;
  }
  r2 -= r1 - 1;
  c2 -= c1 - 1;
  if (isLeftArrow(r1, c1)) {
    return (r2 - c2) / 2;
  } else {
    return (r2 - c2 + 1) / 2;
  }
}

void solve() {
  int n;
  cin >> n;
  vector<int> r(n);
  vector<int> c(n);
  for (int i = 0; i < n; i++) {
    cin >> r[i];
  }
  for (int i = 0; i < n; i++) {
    cin >> c[i];
  }
  vector<pair<int, int>> pts;
  for (int i = 0; i < n; i++) {
    pts.emplace_back(r[i], c[i]);
  }
  sort(pts.begin(), pts.end());
  int curR = 1, curC = 1;
  int res = 0;
  for (auto[nextR, nextC] : pts) {
    res += calcDist(curR, curC, nextR, nextC);
    curR = nextR;
    curC = nextC;
  }
  cout << res << "\n";
}

int main() {
  int tests;
  cin >> tests;
  while (tests-- > 0) {
    solve();
  }
  return 0;
}
```

[1506G - Maximize the Remaining String](/contest/1506/problem/G)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506G - Maximize the Remaining String](/contest/1506/problem/G)

How can you check if you can perform such a sequence of operations on the string $ s$ (latex: $s$) to get the string $ t$ (latex: $t$)? Note that each time we delete an arbitrary character that is repeated at least two times, so $ t$ (latex: $t$) must be a subsequence of the string $ s$ (latex: $s$) and have the same character set as the string $ s$ (latex: $s$).

We will consequently build the resulting string $ t$ (latex: $t$), adding characters to the end. To check if there is such a sequence of operations that turns the string $ s$ (latex: $s$) into the string $ tc?$ (latex: $tc?$) (a string that first contains the characters of the string $ t$ (latex: $t$), then the character $ c$ (latex: $c$), and then some unknown characters), it is enough to do the following: 

 -  Find the minimum index $ i$ (latex: $i$) such that $ t$ (latex: $t$) is included in $ s[\mathrm{1..}i]$ (latex: $s[1..i]$) as a subsequence; 
-  Find the minimum index $ j$ (latex: $j$) ($ i<j$ (latex: $i<j$)) such that $ {s}_{j}=c$ (latex: $s_j = c$); 
-  Then the substring $ s[j+\mathrm{1..}n]$ (latex: $s[j+1..n]$) must contain all characters that are in the string $ s$ (latex: $s$), but which are not in the string $ tc$ (latex: $tc$). 
Let's denote a function that checks the criterion above as $ can(t)$ (latex: $can(t)$).

Having received the verification criterion, the following algorithm can be made: 

 -  Initially $ t$ (latex: $t$) is an empty string; 
-  While there is a character in the string $ s$ (latex: $s$) that is not in the string $ t$ (latex: $t$), we will find the maximum character $ c$ (latex: $c$) not contained in $ t$ (latex: $t$), but contained in $ s$ (latex: $s$), for which $ can(tc)=true$ (latex: $can(tc) = true$) and add it to the end of the string $ t$ (latex: $t$). 
Since at each step we take the maximum symbol for which the criterion is met, the resulting string $ t$ (latex: $t$) will be the lexicographically maximum.

 **Solution** 
```
#include <bits/stdc++.h>
using namespace std;

int distinct(string s) {
  sort(s.begin(), s.end());
  return unique(s.begin(), s.end()) - s.begin();
}

string filter(const string &s, char c) {
  string t;
  bool foundFirst = false;
  for (char a : s) {
    if (a != c && foundFirst) {
      t += a;
    } else if (a == c) {
      foundFirst = true;
    }
  }
  return t;
}

void solve() {
  string s;
  cin >> s;
  int m = distinct(s);
  unordered_set<char> used(s.begin(), s.end());
  string t;
  while (m > 0) {
    char maxC = -1;
    for (char c : used) {
      if (distinct(filter(s, c)) == m - 1) {
        maxC = max(maxC, c);
      }
    }
    t += maxC;
    s = filter(s, maxC);
    used.erase(maxC);
    m--;
  }
  cout << t << "\n";
}

int main() {
  int tests;
  cin >> tests;
  while (tests-- > 0) {
    solve();
  }
  return 0;
}
```
</EDITORIAL>
<ANSWER>
<NAME>
Maximize the Remaining String
</NAME>
<TUTORIAL>
[1506G - Maximize the Remaining String](/contest/1506/problem/G)

Problem author: [MikeMirzayanov](/profile/MikeMirzayanov)

 **Editorial** 
### [1506G - Maximize the Remaining String](/contest/1506/problem/G)

How can you check if you can perform such a sequence of operations on the string $ s$ (latex: $s$) to get the string $ t$ (latex: $t$)? Note that each time we delete an arbitrary character that is repeated at least two times, so $ t$ (latex: $t$) must be a subsequence of the string $ s$ (latex: $s$) and have the same character set as the string $ s$ (latex: $s$).

We will consequently build the resulting string $ t$ (latex: $t$), adding characters to the end. To check if there is such a sequence of operations that turns the string $ s$ (latex: $s$) into the string $ tc?$ (latex: $tc?$) (a string that first contains the characters of the string $ t$ (latex: $t$), then the character $ c$ (latex: $c$), and then some unknown characters), it is enough to do the following: 

 -  Find the minimum index $ i$ (latex: $i$) such that $ t$ (latex: $t$) is included in $ s[\mathrm{1..}i]$ (latex: $s[1..i]$) as a subsequence; 
-  Find the minimum index $ j$ (latex: $j$) ($ i<j$ (latex: $i<j$)) such that $ {s}_{j}=c$ (latex: $s_j = c$); 
-  Then the substring $ s[j+\mathrm{1..}n]$ (latex: $s[j+1..n]$) must contain all characters that are in the string $ s$ (latex: $s$), but which are not in the string $ tc$ (latex: $tc$). 
Let's denote a function that checks the criterion above as $ can(t)$ (latex: $can(t)$).

Having received the verification criterion, the following algorithm can be made: 

 -  Initially $ t$ (latex: $t$) is an empty string; 
-  While there is a character in the string $ s$ (latex: $s$) that is not in the string $ t$ (latex: $t$), we will find the maximum character $ c$ (latex: $c$) not contained in $ t$ (latex: $t$), but contained in $ s$ (latex: $s$), for which $ can(tc)=true$ (latex: $can(tc) = true$) and add it to the end of the string $ t$ (latex: $t$). 
Since at each step we take the maximum symbol for which the criterion is met, the resulting string $ t$ (latex: $t$) will be the lexicographically maximum.

 **Solution** 
```
#include <bits/stdc++.h>
using namespace std;

int distinct(string s) {
  sort(s.begin(), s.end());
  return unique(s.begin(), s.end()) - s.begin();
}

string filter(const string &s, char c) {
  string t;
  bool foundFirst = false;
  for (char a : s) {
    if (a != c && foundFirst) {
      t += a;
    } else if (a == c) {
      foundFirst = true;
    }
  }
  return t;
}

void solve() {
  string s;
  cin >> s;
  int m = distinct(s);
  unordered_set<char> used(s.begin(), s.end());
  string t;
  while (m > 0) {
    char maxC = -1;
    for (char c : used) {
      if (distinct(filter(s, c)) == m - 1) {
        maxC = max(maxC, c);
      }
    }
    t += maxC;
    s = filter(s, maxC);
    used.erase(maxC);
    m--;
  }
  cout << t << "\n";
}

int main() {
  int tests;
  cin >> tests;
  while (tests-- > 0) {
    solve();
  }
  return 0;
}
```
</TUTORIAL>
</ANSWER>