<TARGET>
problem name: Welfare State
</TARGET>
<EDITORIAL>
### [1199A - День города](/contest/1199/problem/A)

$ x$ (latex: $x$) and $ y$ (latex: $y$) are small, so we can explicitly check every day. Complexity $ O(n(x+y))$ (latex: $O(n(x+y))$).

 
### [1199B - Водяная лилия](/contest/1199/problem/B)

We can use Pythagorean theorem and get the equation $ {x}^{2}+{L}^{2}=(H+x{)}^{2}$ (latex: $x^{2} + L^{2} = (H+x)^{2}$). Its solution is $ x=\frac{{L}^{2}-{H}^{2}}{2H}$ (latex: $x=\frac{L^{2}-H^{2}}{2H}$).

 
### [1198A - MP3](/contest/1198/problem/A)

First let's calculate how many different values we can have. Maximal $ k$ (latex: $k$) is $ \frac{8I}{n}$ (latex: $\frac{8I}{n}$), maximal $ K$ (latex: $K$) is $ {2}^{k}$ (latex: $2^{k}$). We have to be careful not to overflow, let's use $ K={2}^{min(20,k)}$ (latex: $K=2^{\min(20, k)}$) ($ {2}^{20}$ (latex: $2^{20}$) is bigger than any $ n$ (latex: $n$)).

Let's sort the array and compress equal values. Now we have to choose no more than $ K$ (latex: $K$) consecutive values in such a way that they cover as much elements as possible. If $ K$ (latex: $K$) is bigger than number of different values, then answer is 0. Otherwise we can precalculate prefix sums and try all the variants to choose $ K$ (latex: $K$) consecutive values.

Complexity is $ O(n\mathrm{log}n)$ (latex: $O(n \log n)$).

 
### [1198B - Welfare State](/contest/1198/problem/B)

For every citizen only the last query of type $ 1$ (latex: $1$) matters. Moreover, all queries before don't matter at all. So the answer for each citizen is maximum of $ x$ (latex: $x$) for last query of type $ 1$ (latex: $1$) for this citizen and maximum of all $ x$ (latex: $x$) for queries of type $ 2$ (latex: $2$) after that. We can calculate maximum $ x$ (latex: $x$) for all suffices of queries of type $ 2$ (latex: $2$), and remember the last query of type $ 1$ (latex: $1$) for each citizen. It can be implemented in $ O(n+q)$ (latex: $O(n+q)$) time.

 
### [1198C - Паросочетание vs независимое множество](/contest/1198/problem/C)

Let's try to take edges to matching greedily in some order. If we can add an edge to the matching (both endpoints are not covered), then we take it. It is easy to see that all vertices not covered by the matching form an independent set — otherwise we would add an edge to the matching. Either matching or independent set has size at least $ n$ (latex: $n$). Complexity — $ O(n+m)$ (latex: $O(n+m)$).

 
### [1198D - Покраска прямоугольника 1](/contest/1198/problem/D)

Let's solve the problem for rectangle $ W\times H$ (latex: $W \times H$) ($ W\ge H$ (latex: $W \ge H$)). Of course, we can cover all rectangle with itself for cost $ W$ (latex: $W$). To get something smaller than $ W$ (latex: $W$) we have to leave at least one column uncovered — otherwise we pay at least sum of $ w$ (latex: $w$) over all rectangles which is at least $ W$ (latex: $W$). This gives us an idea to use DP on rectangles to solve the problem: $ dp[{x}_{1}][{x}_{2}][{y}_{1}][{y}_{2}]$ (latex: $dp[x_{1}][x_{2}][y_{1}][y_{2}]$) is minimal cost to cover the rectangle $ [{x}_{1};{x}_{2})\times [{y}_{1};{y}_{2})$ (latex: $[x_{1};x_{2})\times[y_{1};y_{2})$). It is initialized by $ max({x}_{2}-{x}_{1},{y}_{2}-{y}_{1})$ (latex: $\max(x_{2}-x_{1}, y_{2}-y_{1})$), and we have to try not to cover every column/row. Of course, we have to check if it is all white from the beginning; to do that we will precalculate 2D prefix sums. Total complexity is $ O({n}^{5})$ (latex: $O(n^{5})$).

 
### [1198E - Покраска прямоугольника 2](/contest/1198/problem/E)

If we use some rectangle $ [{x}_{1};{x}_{2})\times [{y}_{1};{y}_{2})$ (latex: $[x_{1};x_{2}) \times [y_{1};y_{2})$) ($ {x}_{2}-{x}_{1}\le {y}_{2}-{y}_{1}$ (latex: $x_{2}-x_{1} \le y_{2}-y_{1}$)), then we can change it to $ [{x}_{1};{x}_{2})\times [0,n)$ (latex: $[x_{1};x_{2}) \times [0, n)$) without changing the cost. Also we can choose $ w$ (latex: $w$) rectangles of width $ 1$ (latex: $1$) instead of one rectangle of width $ w$ (latex: $w$), it will not change the cost.

So, we have to choose minimal number of columns and rows such that all black cells are covered by at least one chosen column/row. If we will build a bipartite graph — left part is columns, right part is rows, there is an edge iff the cell in the intersection of given row and column is black — then the answer is minimal vertex cover in this graph. Minimal vertex cover is the same size as maximum matching, which can be found using flow. All that is left is to see that we can compress identical vertices, and we will have $ O(m)$ (latex: $O(m)$) vertices in both parts.

With Dinic algorithm complexity is $ O({m}^{4})$ (latex: $O(m^{4})$).

 
### [1198F - GCD-группы 2](/contest/1198/problem/F)

All numbers have no more than $ k=9$ (latex: $k=9$) different prime divisors.

If there exist a solution, then for every number there exist a solution in which this number is in group of size not more than $ (k+1)$ (latex: $(k+1)$), because all we have to do is to "kill" all prime numbers from this number, and to do it we only need one number for each prime.

If $ n\le 2(k+1)$ (latex: $n \le 2(k+1)$), we can try all the splits in time $ O({2}^{n}(n+\mathrm{log}C))$ (latex: $O(2^{n} (n + \log C))$).

Let's take two numbers which will be in different groups. How to do it? — let's take random pair. For fixed first number probability of mistake is no more than $ \frac{k}{n-1}$ (latex: $\frac{k}{n-1}$). Now in each group we have to kill no more than $ k$ (latex: $k$) primes. Let's do subset DP — our state is what primes are still alive. This solution has complexity $ O(n{2}^{2k})$ (latex: $O(n 2^{2k})$).

But we actually don't need all $ n$ (latex: $n$) numbers. For each prime we can look at no more than $ 2k$ (latex: $2k$) candidates which can kill it, because to kill all other primes we need strictly less numbers, and we will have a spare one anyways. Thus the solution has complexity $ O({2}^{2k}{k}^{2}+nk)$ (latex: $O(2^{2k}k^{2} + nk)$). We don't need factorization for any numbers except two chosen, and we can factorize them in $ O(\sqrt{C})$ (latex: $O(\sqrt{C})$).
</EDITORIAL>
<ANSWER>
<NAME>
Welfare State
</NAME>
<TUTORIAL>
### [1198B - Welfare State](/contest/1198/problem/B)

For every citizen only the last query of type $ 1$ (latex: $1$) matters. Moreover, all queries before don't matter at all. So the answer for each citizen is maximum of $ x$ (latex: $x$) for last query of type $ 1$ (latex: $1$) for this citizen and maximum of all $ x$ (latex: $x$) for queries of type $ 2$ (latex: $2$) after that. We can calculate maximum $ x$ (latex: $x$) for all suffices of queries of type $ 2$ (latex: $2$), and remember the last query of type $ 1$ (latex: $1$) for each citizen. It can be implemented in $ O(n+q)$ (latex: $O(n+q)$) time.
</TUTORIAL>
</ANSWER>
