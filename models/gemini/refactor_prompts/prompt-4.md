## Name

1334_E. Divisor Paths

## Description

You are given a positive integer D. Let's build the following graph from it: 

  * each vertex is a divisor of D (not necessarily prime, 1 and D itself are also included); 
  * two vertices x and y (x > y) have an undirected edge between them if x is divisible by y and \frac x y is a prime; 
  * the weight of an edge is the number of divisors of x that are not divisors of y. 



For example, here is the graph for D=12: 

<image>

Edge (4,12) has weight 3 because 12 has divisors [1,2,3,4,6,12] and 4 has divisors [1,2,4]. Thus, there are 3 divisors of 12 that are not divisors of 4 — [3,6,12].

There is no edge between 3 and 2 because 3 is not divisible by 2. There is no edge between 12 and 3 because 12/3=4 is not a prime.

Let the length of the path between some vertices v and u in the graph be the total weight of edges on it. For example, path [(1, 2), (2, 6), (6, 12), (12, 4), (4, 2), (2, 6)] has length 1+2+2+3+1+2=11. The empty path has length 0.

So the shortest path between two vertices v and u is the path that has the minimal possible length.

Two paths a and b are different if there is either a different number of edges in them or there is a position i such that a_i and b_i are different edges.

You are given q queries of the following form: 

  * v u — calculate the number of the shortest paths between vertices v and u. 



The answer for each query might be large so print it modulo 998244353.

Input

The first line contains a single integer D (1 ≤ D ≤ 10^{15}) — the number the graph is built from.

The second line contains a single integer q (1 ≤ q ≤ 3 ⋅ 10^5) — the number of queries.

Each of the next q lines contains two integers v and u (1 ≤ v, u ≤ D). It is guaranteed that D is divisible by both v and u (both v and u are divisors of D).

Output

Print q integers — for each query output the number of the shortest paths between the two given vertices modulo 998244353.

Examples

Input


12
3
4 4
12 1
3 4


Output


1
3
1


Input


1
1
1 1


Output


1


Input


288807105787200
4
46 482955026400
12556830686400 897
414 12556830686400
4443186242880 325


Output


547558588
277147129
457421435
702277623

Note

In the first example: 

  * The first query is only the empty path — length 0; 
  * The second query are paths [(12, 4), (4, 2), (2, 1)] (length 3+1+1=5), [(12, 6), (6, 2), (2, 1)] (length 2+2+1=5) and [(12, 6), (6, 3), (3, 1)] (length 2+2+1=5). 
  * The third query is only the path [(3, 1), (1, 2), (2, 4)] (length 1+1+1=3). 

## Editorial

Let's define the semantics of moving along the graph. On each step the current number is either multiplied by some prime or divided by it.

I claim that the all shortest paths from $x$ to $y$ always go through $gcd(x, y)$. Moreover, the vertex numbers on the path first only decrease until $gcd(x, y)$ and only increase after it.

Let's watch what happens to the divisors list on these paths. At first, all the divisors of $x$ that are not divisors of $y$ are removed from the list. Now we reach gcd and we start adding the divisors of $y$ that are missing from the list. The length of the path is this total number of changes to the list. That shows us that these paths are the shortest by definition.

If we ever take a turn off that path, we either will add some divisor that we will need to remove later or remove some divisor that we will need to add later. That makes the length of the path not optimal.

Now let's learn to calculate the number of paths. The parts before gcd and after it will be calculated separately, the answer is the product of answers for both parts.

How many paths are there to gcd? Well, let's divide $x$ by $gcd$, that will give us the primes that should be removed from $x$. You can remove them in any order because the length of the path is always the same. That is just the number of their permutations with repetitions (you might also know that formula as multinomial coefficient).

The number of paths from $gcd$ to $y$ is calculated the same way.

To find the primes in $\frac{x}{gcd(x, y)}$ you can factorize $D$ beforehand and only iterate over the primes of $D$.

Overall complexity: $O(\sqrt{D} + q \log D)$.

## Code

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;
int add(int a, int b){
 a += b;
 if (a >= MOD)
  a -= MOD;
 if (a < 0)
  a += MOD;
 return a;
}
int mul(int a, int b){
 return a * 1ll * b % MOD;
}
int binpow(int a, int b){
 int res = 1;
 while (b){
  if (b & 1)
   res = mul(res, a);
  a = mul(a, a);
  b >>= 1;
 }
 return res;
}
int main() {
 long long d;
 scanf("%lld", &d);
 int q;
 scanf("%d", &q);
 vector<long long> primes;
 for (long long i = 2; i * i <= d; ++i) if (d % i == 0){
  primes.push_back(i);
  while (d % i == 0) d /= i;
 }
 if (d > 1){
  primes.push_back(d);
 }
 vector<int> fact(100), rfact(100);
 fact[0] = 1;
 for (int i = 1; i < 100; ++i)
  fact[i] = mul(fact[i - 1], i);
 rfact[99] = binpow(fact[99], MOD - 2);
 for (int i = 98; i >= 0; --i)
  rfact[i] = mul(rfact[i + 1], i + 1);
 for (int i = 0; i < int(q); i++){
  long long x, y;
  scanf("%lld%lld", &x, &y);
  vector<int> up, dw;
  for (auto p : primes){
   int cnt = 0;
   while (x % p == 0){
    --cnt;
    x /= p;
   }
   while (y % p == 0){
    ++cnt;
    y /= p;
   }
   if (cnt < 0) dw.push_back(-cnt);
   else if (cnt > 0) up.push_back(cnt);
  }
  int ans = 1;
  ans = mul(ans, fact[accumulate(up.begin(), up.end(), 0)]);
  for (auto it : up) ans = mul(ans, rfact[it]);
  ans = mul(ans, fact[accumulate(dw.begin(), dw.end(), 0)]);
  for (auto it : dw) ans = mul(ans, rfact[it]);
  printf("%d\n", ans);
 }
 return 0;
}
```

# Answer

Correct code:

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353;

int add(int a, int b){
 a += b;
 if (a >= MOD)
  a -= MOD;
 if (a < 0)
  a += MOD;
 return a;
}
int mul(int a, int b){
 return a * 1ll * b % MOD;
}
int binpow(int a, int b){
 int res = 1;
 while (b){
  if (b & 1)
   res = mul(res, a);
  a = mul(a, a);
  b >>= 1;
 }
 return res;
}

vector <long long> calculate_prime(long long d) {
  vector<long long> primes;
  for (long long i = 2; i * i <= d; ++i) if (d % i == 0){
   primes.push_back(i);
   while (d % i == 0) d /= i;
  }
  if (d > 1){
   primes.push_back(d);
  }
  return primes;
}

// calculate the factorial for the given number
vector<int> factorial(100);
void calculate_factorial() {
  factorial[0] = 1;
  for (int i = 1; i < 100; ++i)
    factorial[i] = mul(factorial[i - 1], i);
}

// calculate the inverse factorial for the given number
vector<int> inverse_factorial(100);
void calculate_inverse_factorial() {
  inverse_factorial[99] = binpow(factorial[99], MOD - 2);
  for (int i = 98; i >= 0; --i)
    inverse_factorial[i] = mul(inverse_factorial[i + 1], i + 1);
}

// solve each query
void solve_query(const vector<long long>& primes, long long x, long long y) {
  vector<int> up, dw;
  for (auto p : primes){
   int cnt = 0;
   while (x % p == 0){
    --cnt;
    x /= p;
   }
   while (y % p == 0){
    ++cnt;
    y /= p;
   }
   if (cnt < 0) dw.push_back(-cnt);
   else if (cnt > 0) up.push_back(cnt);
  }
  int ans = 1;
  ans = mul(ans, factorial[accumulate(up.begin(), up.end(), 0)]);
  for (auto it : up) ans = mul(ans, inverse_factorial[it]);
  ans = mul(ans, factorial[accumulate(dw.begin(), dw.end(), 0)]);
  for (auto it : dw) ans = mul(ans, inverse_factorial[it]);
  printf("%d\n", ans);
}

int main() {
  long long d;
  scanf("%lld", &d);
  int q;
  scanf("%d", &q);
  auto primes = calculate_prime(d);
  calculate_factorial();
  calculate_inverse_factorial();
  for (int i = 0; i < int(q); i++){
   long long x, y;
   scanf("%lld%lld", &x, &y);
   solve_query(primes, x, y);
  }
  return 0;
}
```

# Compiler Output

OK
