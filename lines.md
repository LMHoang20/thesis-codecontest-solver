<1113_F. Sasha and Interesting Fact from Graph Theory>
<original>
Let's fix $edges$  — the number of edges on the path between $a$ and $b$. Then on this path there are $edges-1$ vertices between $a$ and $b$, and they can be choosen in $A(n - 2, edges - 1)$ ways. The amount of ways to place numbers on edges in such a way, that their sum is equal to $m$, is $\binom{m-1}{edges-1}$ (stars and bars method). If an edge doesn't belong to out path, then doesn't metter what number is written on it, so we can multiply answer by $m^{n-edges-1}$. Now, we want to form a forest from remaining $n-edges-1$ vertices and to hang it to any of $edges + 1$ vertexes from our path. According to one of generalizations of [Cayley's formula](https://en.wikipedia.org/wiki/Cayley's_formula), number of forsests of $x$ vertices, where vertices $1,2, \ldots, y$ belong to different trees is $f(x, y) = y \cdot x^{x - y - 1}$. So for fixed $edges$ we got the formula $trees(edges) = A(n - 2, edges - 1) \cdot f(n, edges + 1) \cdot \binom{m - 1}{edges - 1} \cdot m^{n - edges - 1}$
</original>
<fixed>
Let's fix $edges$  — the number of edges on the path between $a$ and $b$. Then on this path there are $edges-1$ vertices between $a$ and $b$, and they can be choosen in $A(n - 2, edges - 1)$ ways. The amount of ways to place numbers on edges in such a way, that their sum is equal to $m$, is $\binom{m-1}{edges-1}$ (stars and bars method). If an edge doesn't belong to out path, then doesn't metter what number is written on it, so we can multiply answer by $m^{n-edges-1}$. Now, we want to form a forest from remaining $n-edges-1$ vertices and to hang it to any of $edges + 1$ vertexes from our path. According to one of generalizations of Cayley's formula, the number of forests of $x$ vertices, where vertices $1,2, \ldots, y$ belong to different trees is $f(x, y) = y \cdot x^{x - y - 1}$. So for fixed $edges$ we got the formula $trees(edges) = A(n - 2, edges - 1) \cdot f(n, edges + 1) \cdot \binom{m - 1}{edges - 1} \cdot m^{n - edges - 1}$.
</fixed>
</1113_F. Sasha and Interesting Fact from Graph Theory>

<1253_B. Silly Mistake>
<original>
[Implementation](https://pastebin.com/whyCzpvV)
</original>
<fixed>
<remove>[Implementation](https://pastebin.com/whyCzpvV)</remove>
</fixed>
</1253_B. Silly Mistake>

<384_B. Multitasking>
<original>
Code: [http://pastie.org/8651809](http://pastie.org/8651809)
</original>
<fixed>
<remove>Code: [http://pastie.org/8651809](http://pastie.org/8651809)</remove>
</fixed>
</384_B. Multitasking>

<140_E. New Year Garland>
<original>
They would be [Stirling numbers of the second kind](https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind), if there was not a restriction about different colors of consecutive lamps.
</original>
<fixed>
They would be Stirling numbers of the second kind, if there was not a restriction about different colors of consecutive lamps.
</fixed>
</140_E. New Year Garland>

<1293_F. Chaotic V.>
<original>
The proof of this formula is based on the fact this number is calculated through [the sum of the reciprocals of the primes](https://en.wikipedia.org/wiki/Divergence_of_the_sum_of_the_reciprocals_of_the_primes#Proof_that_the_series_exhibits_log-log_growth).
</original>
<fixed>
The proof of this formula is based on the fact this number is calculated through the sum of the reciprocals of the primes.
</fixed>
</1293_F. Chaotic V.>

<477_C. Dreamoon and Strings>
<original>
sample code: [8215203](/contest/476/submission/8215203)
</original>
<fixed>
<remove>sample code: [8215203](/contest/476/submission/8215203)</remove>
</fixed>
</477_C. Dreamoon and Strings>

<350_C. Bombs>
<original>
First of all, Let's sort all point by increasing of value $|x_i| + |y_i|$, all points we will process by using this order. We will process each point greedily, by using maximum six moves. Now we want to come to the point $(x, y)$. Let's $x ≠ 0$. Then we need to move exactly $|x|$ in the $dir$ direction (if $x < 0$ the dir is $L$, $x > 0$ — $R$). Similarly we will work with $y$-coordinates of point $(x, y)$. Now we at the point $(x, y)$, let's pick a bomb at point $(x, y)$. After that we should come back to point $(0, 0)$. Why it is correct to sort all point by increasing of [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry)? If you will look at the path that we have received, you can notice that all points of path have lower Manhattan distance, i.e. we will process this points earlier.
</original>
<fixed>
First of all, Let's sort all point by increasing of value $|x_i| + |y_i|$, all points we will process by using this order. We will process each point greedily, by using maximum six moves. Now we want to come to the point $(x, y)$. Let's $x ≠ 0$. Then we need to move exactly $|x|$ in the $dir$ direction (if $x < 0$ the dir is $L$, $x > 0$ — $R$). Similarly we will work with $y$-coordinates of point $(x, y)$. Now we at the point $(x, y)$, let's pick a bomb at point $(x, y)$. After that we should come back to point $(0, 0)$. Why it is correct to sort all point by increasing of Manhattan distance? If you will look at the path that we have received, you can notice that all points of path have lower Manhattan distance, i.e. we will process this points earlier.
</fixed>
</350_C. Bombs>

<340_E. Iahub and Permutations>
<original>
To sum up in a "LaTeX" way, ![](https://espresso.codeforces.com/c44c16c69547f33183270573042717c9036b496b.png)
</original>
<fixed>
To sum up in a "LaTeX" way, $sol[i] = \binom{fixed}{i} * (tot - i)! - \sum_{j=i+1}^{fixed} sol[j] * \binom{j}{i}$.
</fixed>
</340_E. Iahub and Permutations>

<609_E. Minimum spanning tree for each edge>
<original>
Let's fix some root in the MST (for example the vertex $1$). To find the most heavy edge on the path from $x$ to $y$ we can firstly find the heaviest edge on the path from $x$ to $l = lca(x, y)$ and then on the path from $y$ to $l$, where $l$ is the [lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) of vertices $x$ and $y$. To find $l$ we can use binary lifting method. During calculation of $l$ we also can maintain the weight of the heaviest edge.
</original>
<fixed>
Let's fix some root in the MST (for example the vertex $1$). To find the most heavy edge on the path from $x$ to $y$ we can firstly find the heaviest edge on the path from $x$ to $l = lca(x, y)$ and then on the path from $y$ to $l$, where $l$ is the lowest common ancestor of vertices $x$ and $y$. To find $l$ we can use binary lifting method. During calculation of $l$ we also can maintain the weight of the heaviest edge.
</fixed>
</609_E. Minimum spanning tree for each edge>

<1253_A. Single Push>
<original>
[solution 1](https://pastebin.com/TCAqg38G)
</original>
<fixed>
<remove>[solution 1](https://pastebin.com/TCAqg38G)</remove>
</fixed>
</1253_A. Single Push>

<1168_B. Good Triple>
<original>
[solution](https://pastebin.com/ZJA8Y8Z5)
</original>
<fixed>
<remove>[solution](https://pastebin.com/ZJA8Y8Z5)</remove>
</fixed>
</1168_B. Good Triple>

<887_C. Solution for Cube>
<original>
[Alternative solution](https://pastebin.com/guUQaYKE)
</original>
<fixed>
<remove>[Alternative solution](https://pastebin.com/guUQaYKE)</remove>
</fixed>
</887_C. Solution for Cube>

<535_E. Tavas and Pashmaks>
<original>
[In this code, function `CROSS` returns $(a_x a_y b_x b_y o_x o_y)((1/a_x - 1/o_x, 1/a_y - 1/o_y) \times (1/b_x - 1/o_x, 1/b_y - 1/o_y))$ (it's from order of $10^{16}$, so there won't be any overflows.)](http://ideone.com/ccMHza)
</original>
<fixed>
<remove>[In this code, function `CROSS` returns $(a_x a_y b_x b_y o_x o_y)((1/a_x - 1/o_x, 1/a_y - 1/o_y) \times (1/b_x - 1/o_x, 1/b_y - 1/o_y))$ (it's from order of $10^{16}$, so there won't be any overflows.)](http://ideone.com/ccMHza)</remove>
</fixed>
</535_E. Tavas and Pashmaks>

<1326_E. Bombs>
<original>
[link](https://pastebin.com/A1gFm627)
</original>
<fixed>
<remove>[link](https://pastebin.com/A1gFm627)</remove>
</fixed>
</1326_E. Bombs>

<336_C. Vasily the Bear and Sequence>
<original>
[Author's solution](http://pastebin.com/znNnQF1z)
</original>
<fixed>
<remove>[Author's solution](http://pastebin.com/znNnQF1z)</remove>
</fixed>
</336_C. Vasily the Bear and Sequence>

<1044_D. Deduction Queries>
<original>
Finally, the complexity is $\mathcal{O}(q \log{q})$, but this is only due to the online mapping if we use a regular map; You can use a hash table and get a running time of $\mathcal{O}(q \times \alpha(q))$, but I suggest being careful with a hash table (you may want to read this [blog](https://codeforces.com/blog/entry/62393)).
</original>
<fixed>
Finally, the complexity is $\mathcal{O}(q \log{q})$, but this is only due to the online mapping if we use a regular map; You can use a hash table and get a running time of $\mathcal{O}(q \times \alpha(q))$, but I suggest being careful with a hash table.
</fixed>
</1044_D. Deduction Queries>

<821_E. Okabe and El Psy Kongroo>
<original>
To speed it up, note that the transitions are independent of $x$. This is screaming matrix multiplication! First, if you don't know the matrix exponentiation technique for speeding up DP, you should learn it from [here](https://www.hackerrank.com/topics/matrix-exponentiation).
</original>
<fixed>
To speed it up, note that the transitions are independent of $x$. We can use matrix multiplication.
</fixed>
</821_E. Okabe and El Psy Kongroo>

<385_E. Bear in the Field>
<original>
Power of matrix can be calculated via binary power modulo algo due to associativity of matrix multiplication. More info at [binary_pow](http://e-maxx.ru/algo/binary_pow)
</original>
<fixed>
Power of matrix can be calculated via binary power modulo algo due to associativity of matrix multiplication.
</fixed>
</385_E. Bear in the Field>

<1197_F. Coloring Game>
<original>
What changes if we try to apply the same method to solve the problem with many strips? Unfortunately, we can't analyze each cell as "winning" or "losing" now, we need more information. When solving a problem related to a combination of acyclic games, we may use Sprague-Grundy theory (you can read about it here: [https://cp-algorithms.com/game_theory/sprague-grundy-nim.html](https://cp-algorithms.com/game_theory/sprague-grundy-nim.html)). Instead of marking each cell as "winning" or "losing", we can analyze the Grundy value of each cell. When considering a strip, we should count the number of ways to color it so that its Grundy is exactly $x$ (we should do it for every possible value of $x$), which can help us to solve the initial problem with the following dynamic programming: $z_{i, j}$ is the number of ways to color $i$ first strips so that the Grundy value of their combination is exactly $j$.
</original>
<fixed>
What changes if we try to apply the same method to solve the problem with many strips? Unfortunately, we can't analyze each cell as "winning" or "losing" now, we need more information. When solving a problem related to a combination of acyclic games, we may use Sprague-Grundy theory. Instead of marking each cell as "winning" or "losing", we can analyze the Grundy value of each cell. When considering a strip, we should count the number of ways to color it so that its Grundy is exactly $x$ (we should do it for every possible value of $x$), which can help us to solve the initial problem with the following dynamic programming: $z_{i, j}$ is the number of ways to color $i$ first strips so that the Grundy value of their combination is exactly $j$.
</fixed>
</1197_F. Coloring Game>

<1168_C. And Reachability>
<original>
[solution](https://pastebin.com/QbQa3x4V)
</original>
<fixed>
<remove>[solution](https://pastebin.com/QbQa3x4V)</remove>
</fixed>
</1168_C. And Reachability>

<338_D. GCD Table>
<original>
Finally, let's consider how to solve a system of modular linear equations. We can use an auxiliary method which, given `r1, m1, r2, m2`, finds minimum `X` such that `X = r1 (mod m1)` and `X = r2 (mod m2)`, or determines that such number does not exist. Let `X = m1*x + r1`, then we have `m1*x + r1 = r2 (mod m2)`. This can be represented as a Diophantine equation `m1*x + m2*y = r2-r1` and solved using [Extended Euclidean Algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm). The least non-negative `x`, if it exists, yields the sought `X = m1*x + r1`. Now this method can be used to find the minimum `X1` which satisfies the first two equations. After that, we can say that we have a system with `k-1` equation, where the first two old equations are replaced with a new `j = X1 (mod LCM(a[1], a[2]))`, and repeat the same procedure again. After using this method `k-1` times, we obtain the solution to the whole system.
</original>
<fixed>
Finally, let's consider how to solve a system of modular linear equations. We can use an auxiliary method which, given `r1, m1, r2, m2`, finds minimum `X` such that `X = r1 (mod m1)` and `X = r2 (mod m2)`, or determines that such number does not exist. Let `X = m1*x + r1`, then we have `m1*x + r1 = r2 (mod m2)`. This can be represented as a Diophantine equation `m1*x + m2*y = r2-r1` and solved using Extended Euclidean Algorithm. The least non-negative `x`, if it exists, yields the sought `X = m1*x + r1`. Now this method can be used to find the minimum `X1` which satisfies the first two equations. After that, we can say that we have a system with `k-1` equation, where the first two old equations are replaced with a new `j = X1 (mod LCM(a[1], a[2]))`, and repeat the same procedure again. After using this method `k-1` times, we obtain the solution to the whole system.
</fixed>
</338_D. GCD Table>

<628_F. Bear and Fair Set>
<original>
[The implementation with the Hall's theorem](http://ideone.com/IVZ3Ts)
</original>
<fixed>
<remove>[The implementation with the Hall's theorem](http://ideone.com/IVZ3Ts)</remove>
</fixed>
</628_F. Bear and Fair Set>

<300_A. Array>
<original>
[Аuthor's solution](http://pastebin.com/8aVCeRYx)
</original>
<fixed>
<remove>[Аuthor's solution](http://pastebin.com/8aVCeRYx)</remove>
</fixed>
</300_A. Array>

<590_E. Birthday>
<original>
To solve the second part of the problem one should use the [Dilworth theorem](https://en.wikipedia.org/wiki/Dilworth%27s_theorem). The way to restore the answer subset comes from the constructive proof of the theorem.
</original>
<fixed>
To solve the second part of the problem one should use the Dilworth theorem. The way to restore the answer subset comes from the constructive proof of the theorem.
</fixed>
</590_E. Birthday>

<519_E. A and B and Lecture Rooms>
<original>
$LCA(a, b)$ as [lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) of vertices $a$ and $b$.
</original>
<fixed>
$LCA(a, b)$ as lowest common ancestor of vertices $a$ and $b$.
</fixed>
</519_E. A and B and Lecture Rooms>

<981_D. Bookshelves>
<original>
[solution](https://pastebin.com/hj92UH0B)
</original>
<fixed>
<remove>[solution](https://pastebin.com/hj92UH0B)</remove>
</fixed>
</981_D. Bookshelves>

<1113_E. Sasha and a Patient Friend>
<original>
[Author's solution](https://ideone.com/2jVhHb)
</original>
<fixed>
<remove>[Author's solution](https://ideone.com/2jVhHb)</remove>
</fixed>
</1113_E. Sasha and a Patient Friend>

<887_B. Cubes for Masha>
<original>
[Solution](https://pastebin.com/W5MBrL5e)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/W5MBrL5e)</remove>
</fixed>
</887_B. Cubes for Masha>

<959_A. Mahmoud and Ehab and the even-odd game>
<original>
[https://pastebin.com/X3D08tg9](https://pastebin.com/X3D08tg9)
</original>
<fixed>
<remove>[https://pastebin.com/X3D08tg9](https://pastebin.com/X3D08tg9)</remove>
</fixed>
</959_A. Mahmoud and Ehab and the even-odd game>

<391_F3. Stock Trading>
<original>
After the contest, it has been brought to our attention that this problem has been studied academically. [Here](http://epubl.luth.se/1402-1528/2007/03/LTU-FR-0703-SE.pdf) is the paper describing a linear-time algorithm.
</original>
<fixed>
<remove>After the contest, it has been brought to our attention that this problem has been studied academically. [Here](http://epubl.luth.se/1402-1528/2007/03/LTU-FR-0703-SE.pdf) is the paper describing a linear-time algorithm.</remove>
</fixed>
</391_F3. Stock Trading>

<477_C. Dreamoon and Strings>
<original>
sample code: [8215394](/contest/476/submission/8215394)
</original>
<fixed>
<remove>sample code: [8215394](/contest/476/submission/8215394)</remove>
</fixed>
</477_C. Dreamoon and Strings>

<245_H. Queries for Number of Palindromes>
<original>
After that, $dp[start][start + len - 1]$ can be calculated by the following formula which is derived from [Inc-Exc Principle](https://en.wikipedia.org/wiki/Inclusion-exclusion_principle).
</original>
<fixed>
After that, $dp[start][start + len - 1]$ can be calculated by the following formula which is derived from the inclusion-exclusion principle.
</fixed>
</245_H. Queries for Number of Palindromes>

<1288_F. Red-Blue Graph>
<original>
How to deal with edges such that there should be some flow along them? You may use classic "flows with demands" approach from here: [https://cp-algorithms.com/graph/flow_with_demands.html](https://cp-algorithms.com/graph/flow_with_demands.html). Or you can model it with the help of the costs: if the flow along the edge should be between $l$ and $r$, we can add two edges: one with capacity $l$ and cost $k$ (where $k$ is a negative number with sufficiently large absolute value, for example, $-10^9$), and another with capacity $r - l$ and cost $0$.
</original>
<fixed>
How to deal with edges such that there should be some flow along them? You may use classic "flows with demands" approach. Or you can model it with the help of the costs: if the flow along the edge should be between $l$ and $r$, we can add two edges: one with capacity $l$ and cost $k$ (where $k$ is a negative number with sufficiently large absolute value, for example, $-10^9$), and another with capacity $r - l$ and cost $0$.
</fixed>
</1288_F. Red-Blue Graph>

<1504_A.  Déjà Vu>
<original>
[Implementation](https://codeforces.com/contest/1504/submission/111950211)
</original>
<fixed>
<remove>[Implementation](https://codeforces.com/contest/1504/submission/111950211)</remove>
</fixed>
</1504_A.  Déjà Vu>

<340_E. Iahub and Permutations>
<original>
This recurrences can be computed by classical dp or by memoization. I'll present [DamianS](/profile/DamianS)'s source, which used memoization. As you can see, it's very short and easy to implement. [Link](http://pastie.org/8286348)
</original>
<fixed>
This recurrences can be computed by classical dp or by memoization. It's very short and easy to implement with memoization. <remove>[solution using memoization](http://pastie.org/8286348)</remove>
</fixed>
</340_E. Iahub and Permutations>

<975_D. Ghosts>
<original>
[Solution](https://pastebin.com/AKd4c5xt)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/AKd4c5xt)</remove>
</fixed>
</975_D. Ghosts>

<887_E. Little Brother>
<original>
[Solution.](https://pastebin.com/1Qkef8JL)
</original>
<fixed>
<remove>[Solution.](https://pastebin.com/1Qkef8JL)</remove>
</fixed>
</887_E. Little Brother>

<340_E. Iahub and Permutations>
<original>
We iterate now an index *i* from *fixed* to 0. Let sol[i] = the number of possible permutations having *exactly*  *i* fixed points. Obviously, sol[0] is the answer to our problem. Let's introduce a [combination](https://en.wikipedia.org/wiki/Combination) ![](https://espresso.codeforces.com/a4b0ae77c1b1e95e3cba7276cfb7fecdb99b4221.png) representing in how many ways I can choose k objects out of n. I have list of positions which can be transformed into fix points (they are *fixed* positions). I need to choose *i* of them. According to the above definition, I get sol[i] = ![](https://espresso.codeforces.com/4cbfc413bd52e416b1fb7c018581f2467cb5a712.png) . Next, I have to fill *tot* - *i* positions with remained elements. We'll consider for this moment valid each permutation of not used values. So, sol[i] = ![](https://espresso.codeforces.com/37e8612bbe476531470cec72cae3f7df22b9b162.png) . Where is the problem to this formula?
</original>
<fixed>
We iterate now an index *i* from *fixed* to 0. Let sol[i] = the number of possible permutations having *exactly*  *i* fixed points. Obviously, sol[0] is the answer to our problem. Let's introduce a combination *n choose k* representing in how many ways I can choose k objects out of n. I have list of positions which can be transformed into fix points (they are *fixed* positions). I need to choose *i* of them. According to the above definition, I get *sol[i]* = *fixed* choose *i*. Next, I have to fill *tot* - *i* positions with remained elements. We'll consider for this moment valid each permutation of not used values. So, *sol[i]* = (*fixed* choose *i*) * (*tot* - *i*)!. Where is the problem to this formula?
</fixed>
</340_E. Iahub and Permutations>

<332_C. Students' Revenge>
<original>
[Code](http://pastebin.com/CzB1v72v)
</original>
<fixed>
<remove>[Code](http://pastebin.com/CzB1v72v)</remove>
</fixed>
</332_C. Students' Revenge>

<138_D. World of Darkraft>
<original>
Notice that the game can be separated into two independent: for only even and only odd coordinate sum cells. The player chooses the game he would like to make a move in. Thus, if we find a [Grundy function](https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem) for each of this games we can find the whole game result.
</original>
<fixed>
Notice that the game can be separated into two independent: for only even and only odd coordinate sum cells. The player chooses the game he would like to make a move in. Thus, if we find a Grundy function for each of this games we can find the whole game result.
</fixed>
</138_D. World of Darkraft>

<911_D. Inversion Counting>
<original>
Permutaion with one swap is called transposition. Any permutation can be expressed as the composition (product) of transpositions. Simpler, you can get any permutation from any other one of the same length by doing some number of swaps. The sign of the permutation is the number of transpositions needed to get it from the identity permutation. Luckily (not really, this is pure math, check out all proofs at [wiki](https://en.wikipedia.org/wiki/Parity_of_a_permutation), e.g) the sign can also tell us the parity of inversion count. 
</original>
<fixed>
Permutaion with one swap is called transposition. Any permutation can be expressed as the composition (product) of transpositions. Simpler, you can get any permutation from any other one of the same length by doing some number of swaps. The sign of the permutation is the number of transpositions needed to get it from the identity permutation. Luckily, the sign can also tell us the parity of inversion count. 
</fixed>
</911_D. Inversion Counting>

<975_E. Hag's Khashba>
<original>
[Solution](https://pastebin.com/4VmUcVUR)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/4VmUcVUR)</remove>
</fixed>
</975_E. Hag's Khashba>

<1168_D. Anagram Paths>
<original>
[solution](https://pastebin.com/5bwnF7En)
</original>
<fixed>
<remove>[solution](https://pastebin.com/5bwnF7En)</remove>
</fixed>
</1168_D. Anagram Paths>

<332_A. Down the Hatch!>
<original>
[code](http://pastebin.com/hn4wzXj0)
</original>
<fixed>
<remove>[code](http://pastebin.com/hn4wzXj0)</remove>
</fixed>
</332_A. Down the Hatch!>

<475_F. Meta-universe>
<original>
That is the entire solution, I'd like to get back one more time to the complexity analysis. We have a recurring algorithm, on every step of the recurrence we're looking for the split point, then we split and invoke this recurring algorithm two more times. It looks that for the worst case (which is split in the middle) we will split a sequence into two subsequences of the same size, so we have a full right to apply a [Master theorem](https://en.wikipedia.org/wiki/Master_theorem) here. On each step our complexity seems to be $O(NlogN)$.
</original>
<fixed>
That is the entire solution, I'd like to get back one more time to the complexity analysis. We have a recurring algorithm, on every step of the recurrence we're looking for the split point, then we split and invoke this recurring algorithm two more times. It looks that for the worst case (which is split in the middle) we will split a sequence into two subsequences of the same size, so we have a full right to apply a Master theorem here. On each step our complexity seems to be $O(NlogN)$.
</fixed>
</475_F. Meta-universe>

<547_E. Mike and Friends>
<original>
This problem is just like [KQUERY](http://www.spoj.com/problems/KQUERY/). It uses segment tree, but you can also use Fenwick instead of segment tree.
</original>
<fixed>
This problem is just like the problem where you are given a sequence of n numbers a1, a2, ..., an and a number of k-queries. A k-query is a triple (i, j, k) (1 ≤ i ≤ j ≤ n). For each k-query (i, j, k), you have to return the number of elements greater than k in the subsequence ai, ai+1, ..., aj. It can be solved using segment tree, but you can also use Fenwick instead of segment tree.
</fixed>
</547_E. Mike and Friends>

<340_A. The Wall>
<original>
Official solution: [4383403](/contest/340/submission/4383403)
</original>
<fixed>
<remove>Official solution: [4383403](/contest/340/submission/4383403)</remove>
</fixed>
</340_A. The Wall>

<1113_D. Sasha and One More Name>
<original>
[Author's solution](https://ideone.com/5XG0Bp)
</original>
<fixed>
<remove>[Author's solution](https://ideone.com/5XG0Bp)</remove>
</fixed>
</1113_D. Sasha and One More Name>

<1253_C. Sweets Eating>
<original>
[Implementation](https://pastebin.com/3hZLq6sP)
</original>
<fixed>
<remove>[Implementation](https://pastebin.com/3hZLq6sP)</remove>
</fixed>
</1253_C. Sweets Eating>

<271_D. Good Substrings>
<original>
There is also an easier solution, where instead of trie we use [Rabin-Karp rolling hash](https://en.wikipedia.org/wiki/Rolling_hash) to count substrings that differ by content. Just sort the hashes of all good substrings and find the number of unique hashes (equal hashes will be on adjacent positions after sort). But these hashes are unreliable in general, so it's always better to use precise algorithm.
</original>
<fixed>
There is also an easier solution, where instead of trie we use Rabin-Karp rolling hash to count substrings that differ by content. Just sort the hashes of all good substrings and find the number of unique hashes (equal hashes will be on adjacent positions after sort). But these hashes are unreliable in general, so it's always better to use precise algorithm.
</fixed>
</271_D. Good Substrings>

<330_B. Road Construction>
<original>
- The constraints can be satisfied if and only if the graph is a [Star Graph](https://en.wikipedia.org/wiki/Star_%28graph_theory%29). We can just create a star graph centered with the node and connect it to all other nodes.
</original>
<fixed>
- The constraints can be satisfied if and only if the graph is a Star Graph. We can just create a star graph centered with the node and connect it to all other nodes.
</fixed>
</330_B. Road Construction>

<859_E. Desk Disorder>
<original>
To compute the result, we can use a [Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure). For each connected component, we keep track of its size and what type of cycle (if any) is present. Initially each desk is in a component by itself. For each engineer, we merge the components containing their current and desired desks, or mark the component as containing a cycle if the current and desired desks were already in the same component. Finally we multiply together the numbers of assignments of the components.
</original>
<fixed>
To compute the result, we can use a Disjoint-set data structure. For each connected component, we keep track of its size and what type of cycle (if any) is present. Initially each desk is in a component by itself. For each engineer, we merge the components containing their current and desired desks, or mark the component as containing a cycle if the current and desired desks were already in the same component. Finally we multiply together the numbers of assignments of the components.
</fixed>
</859_E. Desk Disorder>

<271_D. Good Substrings>
<original>
At first, build a [trie](https://en.wikipedia.org/wiki/Trie) containing all suffixes of given string (this structure is also called explicit suffix tree). Let's iterate over all substrings in order of indexes' increasing, i. e. first $[1...1], $ then $[1...2], [1...3], ..., [1...n], [2...2], [2...3], ..., [2...n], ...$ Note, that moving from a substring to the next one is just adding a single character to the end. So we can easily maintain the number of bad characters, and also the "current" node in the trie. If the number of bad characters doesn't exceed $k$, then the substring is good. And we need to mark the corresponding node of trie, if we never did this before. The answer will be the number of marked nodes in the trie.
</original>
<fixed>
At first, build a trie containing all suffixes of given string (this structure is also called explicit suffix tree). Let's iterate over all substrings in order of indexes' increasing, i. e. first $[1...1], $ then $[1...2], [1...3], ..., [1...n], [2...2], [2...3], ..., [2...n], ...$ Note, that moving from a substring to the next one is just adding a single character to the end. So we can easily maintain the number of bad characters, and also the "current" node in the trie. If the number of bad characters doesn't exceed $k$, then the substring is good. And we need to mark the corresponding node of trie, if we never did this before. The answer will be the number of marked nodes in the trie.
</fixed>
</271_D. Good Substrings>

<975_A. Aramic script>
<original>
[Solution](https://pastebin.com/XUUxYdqB)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/XUUxYdqB)</remove>
</fixed>
</975_A. Aramic script>

<981_H. K Paths>
<original>
[Solution in $O(n \sqrt n)$](https://pastebin.com/b3h4M9rL) 
</original>
<fixed>
<remove>[Solution in $O(n \sqrt n)$](https://pastebin.com/b3h4M9rL)</remove>
</fixed>
</981_H. K Paths>

<1113_C. Sasha and a Bit of Relax>
<original>
[Author's solution](https://ideone.com/Jf8Za8)
</original>
<fixed>
<remove>[Author's solution](https://ideone.com/Jf8Za8)</remove>
</fixed>
</1113_C. Sasha and a Bit of Relax>

<439_E. Devu and Birthday Celebration>
<original>
Now you have to use [Möbius inversion formula.](https://en.wikipedia.org/wiki/M%C3%B6bius_inversion_formula)
</original>
<fixed>
Now you have to use Möbius inversion formula.
</fixed>
</439_E. Devu and Birthday Celebration>

<338_A. Quiz>
<original>
The abovementioned observation shows that the minimum score grows monotonically when `X` is increased, so all we need is to find the minimum feasible `X`. It should satisfy the inequalities `X*k <= n` and `X + (n - n mod k) / k * (k-1) + n mod k >= m`. More on the second inequality: Manao answered the first `X*k` questions, thus there are `n-X*k` left. Now he can answer at most `k-1` question from each `k` questions. If `k` divides `n-X*k` (which is the same as `k` divides `n`), the inequality becomes `X*k + (n-X*k) / k * (k-1) >= m`, but the remainder complicates it a bit: `X*k + (n - X*k - (n - X*k) mod k) / k * (k-1) + (n - X*k) mod k >= m`. This formula can be simplified to the one written earlier. So, the minimum `X` is equal to `max(0, m - (n - n mod k) / k * (k-1) - n mod k)`. You'll need [exponentiation by squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring) to compute the score corresponding to this value of `X`. Thus, the overall complexity of this solution is `O(log(n))`.
</original>
<fixed>
The abovementioned observation shows that the minimum score grows monotonically when `X` is increased, so all we need is to find the minimum feasible `X`. It should satisfy the inequalities `X*k <= n` and `X + (n - n mod k) / k * (k-1) + n mod k >= m`. More on the second inequality: Manao answered the first `X*k` questions, thus there are `n-X*k` left. Now he can answer at most `k-1` question from each `k` questions. If `k` divides `n-X*k` (which is the same as `k` divides `n`), the inequality becomes `X*k + (n-X*k) / k * (k-1) >= m`, but the remainder complicates it a bit: `X*k + (n - X*k - (n - X*k) mod k) / k * (k-1) + (n - X*k) mod k >= m`. This formula can be simplified to the one written earlier. So, the minimum `X` is equal to `max(0, m - (n - n mod k) / k * (k-1) - n mod k)`. You'll need exponentiation by squaring to compute the score corresponding to this value of `X`. Thus, the overall complexity of this solution is `O(log(n))`.
</fixed>
</338_A. Quiz>

<336_D. Vasily the Bear and Beautiful Strings>
<original>
[Author's solution](http://pastebin.com/2cZ2qefM)
</original>
<fixed>
<remove>[Author's solution](http://pastebin.com/2cZ2qefM)</remove>
</fixed>
</336_D. Vasily the Bear and Beautiful Strings>

<887_A. Div. 64>
<original>
[Solution](https://pastebin.com/mKYmrrnm)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/mKYmrrnm)</remove>
</fixed>
</887_A. Div. 64>

<123_D. String>
<original>
[The author's solution](/contest/123/submission/835591)
</original>
<fixed>
<remove>[The author's solution](/contest/123/submission/835591)</remove>
</fixed>
</123_D. String>

<981_F. Round Marriage>
<original>
[Solution in $O(n \cdot log L \cdot log n)$](https://pastebin.com/Q7LKS1rN)
</original>
<fixed>
<remove>[Solution in $O(n \cdot log L \cdot log n)$](https://pastebin.com/Q7LKS1rN)</remove>
</fixed>
</981_F. Round Marriage>

<340_B. Maximal Area Quadrilateral>
<original>
Official solution: [4383413](/contest/340/submission/4383413)
</original>
<fixed>
<remove>Official solution: [4383413](/contest/340/submission/4383413)</remove>
</fixed>
</340_B. Maximal Area Quadrilateral>

<391_C3. The Tournament>
<original>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. If you are not familiar with using bitmasks, I recommend reading the old-but-never-outdated [tutorial](http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=bitManipulation) by [bmerry](/profile/bmerry) and [dimkadimon](/profile/dimkadimon)'s Topcoder Cookbook [recipe](http://apps.topcoder.com/forums/?module=Thread&threadID=671150&start=0) on iterating over subsets. This is a pseudocode showing how short a bitmask solution for this problem is:
</original>
<fixed>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. This is a pseudocode showing how short a bitmask solution for this problem is:
</fixed>
</391_C3. The Tournament>

<1097_G. Vladislav and a Great Legend>
<original>
Firstly, to properly understand what does "calculate the sum of the $k$-th powers" means, I recommend you to get acquainted with these two lectures (especially the "powers technique"): [Sums and Expected Value — part 1](https://codeforces.com/blog/entry/62690), [Sums and Expected Value — part 2](https://codeforces.com/blog/entry/62792).
</original>
<fixed>
<remove>Firstly, to properly understand what does "calculate the sum of the $k$-th powers" means, I recommend you to get acquainted with these two lectures (especially the "powers technique"): [Sums and Expected Value — part 1](https://codeforces.com/blog/entry/62690), [Sums and Expected Value — part 2](https://codeforces.com/blog/entry/62792).</remove>
</fixed>
</1097_G. Vladislav and a Great Legend>

<384_E. Propagating tree>
<original>
Code (actually we use just one Fenwick tree instead of 2, can you think why it works? :) ) : [http://pastie.org/8651824](http://pastie.org/8651824)
</original>
<fixed>
<remove>Code (actually we use just one Fenwick tree instead of 2, can you think why it works? :) ) : [http://pastie.org/8651824](http://pastie.org/8651824)</remove>
</fixed>
</384_E. Propagating tree>

<559_D. Randomizer>
<original>
We can use [Pick's theorem](https://en.wikipedia.org/wiki/Pick%27s_theorem) for calculate integer points number in every polygon. Integer points number on the segment between points $(0, 0)$ and $(a, b)$ one can calculate over $GCD(a, b)$.
</original>
<fixed>
We can use Pick's theorem for calculate integer points number in every polygon. Integer points number on the segment between points $(0, 0)$ and $(a, b)$ one can calculate over $GCD(a, b)$.
</fixed>
</559_D. Randomizer>

<300_B. Coach>
<original>
[Аuthor's solution](http://pastebin.com/2q8CThPh)
</original>
<fixed>
<remove>[Аuthor's solution](http://pastebin.com/2q8CThPh)</remove>
</fixed>
</300_B. Coach>

<981_G. Magic multisets>
<original>
[Solution](https://pastebin.com/LqzHXKkj)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/LqzHXKkj)</remove>
</fixed>
</981_G. Magic multisets>

<1136_B. Nastya Is Playing Computer Games>
<original>
[Code](https://pastebin.com/19BUreFe)
</original>
<fixed>
<remove>[Code](https://pastebin.com/19BUreFe)</remove>
</fixed>
</1136_B. Nastya Is Playing Computer Games>

<1534_G. A New Beginning>
<original>
This dp can then be optimized using slope trick. If you are not familiar with slope trick, we recommend learning it first at [Slope trick explained](https://codeforces.com/blog/entry/77298) and [Slope Trick](https://codeforces.com/blog/entry/47821). 
</original>
<fixed>
This dp can then be optimized using slope trick.<remove>If you are not familiar with slope trick, we recommend learning it first at [Slope trick explained](https://codeforces.com/blog/entry/77298) and [Slope Trick](https://codeforces.com/blog/entry/47821).</remove>
</fixed>
</1534_G. A New Beginning>

<336_B. Vasily the Bear and Fly>
<original>
[Author's solution](http://pastebin.com/iTr4213i)
</original>
<fixed>
<remove>[Author's solution](http://pastebin.com/iTr4213i)</remove>
</fixed>
</336_B. Vasily the Bear and Fly>

<409_D. Big Data>
<original>
A lot of facts with big numbers is not yet big data. Especially if half of them are wrong! The biggest board games tournament had 43 thousand chess players, the math competition — over a million participants, and Colonel Meow, while a gorgeous cat (you can enjoy the photos at [Guinness World Records site](http://www.guinnessworldrecords.com/world-records/size/longest-fur-on-a-cat) ), still doesn't feature a meter-long fur!
</original>
<fixed>
<remove>A lot of facts with big numbers is not yet big data. Especially if half of them are wrong! The biggest board games tournament had 43 thousand chess players, the math competition — over a million participants, and Colonel Meow, while a gorgeous cat (you can enjoy the photos at [Guinness World Records site](http://www.guinnessworldrecords.com/world-records/size/longest-fur-on-a-cat) ), still doesn't feature a meter-long fur!</remove>
</fixed>
</409_D. Big Data>

<1253_F. Cheap Robot>
<original>
[Solution 2](https://pastebin.com/J8c8x2Fg)
</original>
<fixed>
<remove>[Solution 2](https://pastebin.com/J8c8x2Fg)</remove>
</fixed>
</1253_F. Cheap Robot>

<540_D. Bad Luck Island>
<original>
[code](http://pastebin.com/3s6dRK3A)
</original>
<fixed>
<remove>[code](http://pastebin.com/3s6dRK3A)</remove>
</fixed>
</540_D. Bad Luck Island>

<631_A. Interview>
<original>
You should know only one fact to solve this task: $X \vee Y \geq X$. This fact can be proved by the [truth table](https://en.wikipedia.org/wiki/Truth_table). Let's use this fact: $f(a, 1, i-1) \vee f(a, i, j) \vee f(a, j+1, N) \geq f(a, i, j)$. Also $f(a, 1, i-1) \vee f(a, i, j) \vee f(a, j+1, n) = f(a, 1, n)$. According two previous formulas we can get that $f(a, 1, n) ≥ f(a, i, j)$. Finally we can get the answer. It's equal to $f(a, 1, N) + f(b, 1, N)$.
</original>
<fixed>
You should know only one fact to solve this task: $X \vee Y \geq X$. This fact can be proved by the truth table. Let's use this fact: $f(a, 1, i-1) \vee f(a, i, j) \vee f(a, j+1, N) \geq f(a, i, j)$. Also $f(a, 1, i-1) \vee f(a, i, j) \vee f(a, j+1, n) = f(a, 1, n)$. According two previous formulas we can get that $f(a, 1, n) ≥ f(a, i, j)$. Finally we can get the answer. It's equal to $f(a, 1, N) + f(b, 1, N)$.
</fixed>
</631_A. Interview>

<1253_E. Antenna Coverage>
<original>
[Implementation](https://pastebin.com/6FeZb3XH)
</original>
<fixed>
<remove>[Implementation](https://pastebin.com/6FeZb3XH)</remove>
</fixed>
</1253_E. Antenna Coverage>

<812_E. Sagheer and Apple Tree>
<original>
You can read more about games from [this link](http://e-maxx.ru/algo/sprague_grundy)
</original>
<fixed>
<remove>You can read more about games from [this link](http://e-maxx.ru/algo/sprague_grundy)</remove>
</fixed>
</812_E. Sagheer and Apple Tree>

<509_A. Maximum in Table>
<original>
One may see the [Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) in the given matrix and understand that answer is equal to $2n - 2 \choose n - 1$.
</original>
<fixed>
One may see the Pascal's triangle in the given matrix and understand that answer is equal to $2n - 2 \choose n - 1$.
</fixed>
</509_A. Maximum in Table>

<393_B. Three matrices>
<original>
By the way, there is some interesting math connected to this problem: [link](https://en.wikipedia.org/wiki/Symmetric_matrix#Decomposition_into_symmetric_and_skew-symmetric)
</original>
<fixed>
<remove>By the way, there is some interesting math connected to this problem: [link](https://en.wikipedia.org/wiki/Symmetric_matrix#Decomposition_into_symmetric_and_skew-symmetric)</remove>
</fixed>
</393_B. Three matrices>

<385_C. Bear and Prime Numbers>
<original>
It can be seen that given algo is very similar to Sieve of Eratosthenes. (Info here [eratosthenes sieve](http://e-maxx.ru/algo/eratosthenes_sieve)) So we can use this algo if we change it a little bit. Also, we will store results of calculation in array, e.g. $pre$. Namely, $pre[n] = f(n)$.
</original>
<fixed>
It can be seen that given algo is very similar to Sieve of Eratosthenes. So we can use this algo if we change it a little bit. Also, we will store results of calculation in array, e.g. $pre$. Namely, $pre[n] = f(n)$.
</fixed>
</385_C. Bear and Prime Numbers>

<622_F. The Sum of the k-th Powers>
<original>
Denote $P_x$ the value of the sum for $n = x$. We can easily calculate the values of $P_x$ for $x$ from $0$ to $k + 1$ in $O(klogk)$ time. If $n < k + 2$ then we already have the answer. Otherwise let's use [Lagrange polynomial](https://en.wikipedia.org/wiki/Lagrange_polynomial) to get the value of the sum for the given value $n$.
</original>
<fixed>
Denote $P_x$ the value of the sum for $n = x$. We can easily calculate the values of $P_x$ for $x$ from $0$ to $k + 1$ in $O(klogk)$ time. If $n < k + 2$ then we already have the answer. Otherwise let's use Lagrange polynomial to get the value of the sum for the given value $n$.
</fixed>
</622_F. The Sum of the k-th Powers>

<981_C. Useful Decomposition>
<original>
[solution](https://pastebin.com/ybnP74S0)
</original>
<fixed>
<remove>[solution](https://pastebin.com/ybnP74S0)</remove>
</fixed>
</981_C. Useful Decomposition>

<384_A. Coder>
<original>
Code: [http://pastie.org/8651801](http://pastie.org/8651801)
</original>
<fixed>
<remove>[http://pastie.org/8651801](http://pastie.org/8651801)</remove>
</fixed>
</384_A. Coder>

<1136_A. Nastya Is Reading a Book>
<original>
[Code](https://pastebin.com/caetUqwX)
</original>
<fixed>
<remove>[Code](https://pastebin.com/caetUqwX)</remove>
</fixed>
</1136_A. Nastya Is Reading a Book>

<391_C2. The Tournament>
<original>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. If you are not familiar with using bitmasks, I recommend reading the old-but-never-outdated [tutorial](http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=bitManipulation) by [bmerry](/profile/bmerry) and [dimkadimon](/profile/dimkadimon)'s Topcoder Cookbook [recipe](http://apps.topcoder.com/forums/?module=Thread&threadID=671150&start=0) on iterating over subsets. This is a pseudocode showing how short a bitmask solution for this problem is:
</original>
<fixed>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. This is a pseudocode showing how short a bitmask solution for this problem is:
</fixed>
</391_C2. The Tournament>

<391_C1. The Tournament>
<original>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. If you are not familiar with using bitmasks, I recommend reading the old-but-never-outdated [tutorial](http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=bitManipulation) by [bmerry](/profile/bmerry) and [dimkadimon](/profile/dimkadimon)'s Topcoder Cookbook [recipe](http://apps.topcoder.com/forums/?module=Thread&threadID=671150&start=0) on iterating over subsets. This is a pseudocode showing how short a bitmask solution for this problem is:
</original>
<fixed>
How can we generate all scenarios? A natural way to do this is recursion: for each fight, we choose the outcome (win or loss) and recurse one level deeper, stopping when all match outcomes have been chosen and performing the evaluation. However, there is another way which is usually less time-consuming: bitmasks. This is a pseudocode showing how short a bitmask solution for this problem is:
</fixed>
</391_C1. The Tournament>

<501_D. Misha and Permutations Summation>
<original>
To solve the problem, one need to be able to find the index of given permutation in lexicographical order and permutation by its index. We will store indices in factorial number system. Thus number $x$ is represented as $\sum_{k=1}^{n} d_k \times k!$. You can find the rules of the transform [here](https://en.wikipedia.org/wiki/Factorial_number_system).
</original>
<fixed>
To solve the problem, one need to be able to find the index of given permutation in lexicographical order and permutation by its index. We will store indices in factorial number system. Thus number $x$ is represented as $\sum_{k=1}^{n} d_k \times k!$.
</fixed>
</501_D. Misha and Permutations Summation>

<946_F. Fibonacci String Subsequences>
<original>
[https://pastebin.com/ctSVxmnD](https://pastebin.com/ctSVxmnD)
</original>
<fixed>
<remove>[https://pastebin.com/ctSVxmnD](https://pastebin.com/ctSVxmnD)</remove>
</fixed>
</946_F. Fibonacci String Subsequences>

<1136_E. Nastya Hasn't Written a Legend>
<original>
[Code](https://pastebin.com/nGFM2KyW)
</original>
<fixed>
<remove>[Code](https://pastebin.com/nGFM2KyW)</remove>
</fixed>
</1136_E. Nastya Hasn't Written a Legend>

<1168_A. Increasing by Modulo>
<original>
[This solution](https://pastebin.com/dDf2JKNd)
</original>
<fixed>
<remove>[This solution](https://pastebin.com/dDf2JKNd)</remove>
</fixed>
</1168_A. Increasing by Modulo>

<123_C. Brackets>
<original>
[The author's solution](/contest/123/submission/835590)
</original>
<fixed>
<remove>[The author's solution](/contest/123/submission/835590)</remove>
</fixed>
</123_C. Brackets>

<585_C. Alice, Bob, Oranges and Apples>
<original>
Firstly, let's understand the process described in problem statement. If one would write a tree of a sum-pairs $(x, y)$ with letters $A$ and $B$, he would get the [Stern–Brocot tree](https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree). Let the number of oranges be enumerator and the number of apples be denumerator of fraction. At every step we have two fractions (at first step they are $\frac{0}{1} \frac{1}{0}$) and should replace exactly one of them with their mediant. In such way first fraction is first parent to the left from mediant while second fraction is parent to the right. The process described in statement is, this way, a process of finding a fraction in the Stern-Brocot tree, finishing when the current mediant is equal to current node in the tree and $(x, y)$ pair is the fraction we are searching. 
</original>
<fixed>
Firstly, let's understand the process described in problem statement. If one would write a tree of a sum-pairs $(x, y)$ with letters $A$ and $B$, he would get the Stern–Brocot tree. Let the number of oranges be enumerator and the number of apples be denumerator of fraction. At every step we have two fractions (at first step they are $\frac{0}{1} \frac{1}{0}$) and should replace exactly one of them with their mediant. In such way first fraction is first parent to the left from mediant while second fraction is parent to the right. The process described in statement is, this way, a process of finding a fraction in the Stern-Brocot tree, finishing when the current mediant is equal to current node in the tree and $(x, y)$ pair is the fraction we are searching. 
</fixed>
</585_C. Alice, Bob, Oranges and Apples>

<1025_G. Company Acquisitions>
<original>
To prove this more rigorously, we can use show that this process is a martingale, so we can use [Optional stopping theorem](https://en.wikipedia.org/wiki/Optional_stopping_theorem) to show that the expected number of days is exactly equal to this difference.
</original>
<fixed>
To prove this more rigorously, we can use show that this process is a martingale, so we can use Optional stopping theorem to show that the expected number of days is exactly equal to this difference.
</fixed>
</1025_G. Company Acquisitions>

<850_C. Arpa and a game with Mojtaba>
<original>
The problem is separate for each prime, so we will calculate [Grundy number](https://en.wikipedia.org/wiki/Grundy_number) for each prime and xor these number to find the answer.
</original>
<fixed>
The problem is separate for each prime, so we will calculate Grundy number for each prime and xor these number to find the answer.
</fixed>
</850_C. Arpa and a game with Mojtaba>

<590_E. Birthday>
<original>
To build the graph one can use [Aho-Corasick](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm) algorithm. Usage of this structure allow to build all essential arc of the graph in time $O(L)$, where $L$ stands for the total length of all strings in the input. We will call the arc $u v \in E$ essential, if there is no $w$, such that $u w \in E$ and $w v \in E$. One of the ways to do so is: 
</original>
<fixed>
To build the graph one can use Aho-Corasick algorithm. Usage of this structure allow to build all essential arc of the graph in time $O(L)$, where $L$ stands for the total length of all strings in the input. We will call the arc $u v \in E$ essential, if there is no $w$, such that $u w \in E$ and $w v \in E$. One of the ways to do so is: 
</fixed>
</590_E. Birthday>

<515_E. Drazil and Park>
<original>
More information about RMQ: [editorial](http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=lowestCommonAncestor#Sparse_Table_%28ST%29_algorithm) from Topcoder
</original>
<fixed>
<remove>More information about RMQ: [editorial](http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=lowestCommonAncestor#Sparse_Table_%28ST%29_algorithm) from Topcoder</remove>
</fixed>
</515_E. Drazil and Park>

<453_D. Little Pony and Elements of Harmony>
<original>
We notice that the eigenvalue is only related to the number of ones in $i$, and it is not hard to calc one eigenvalue in $O(m)$ time. To decompose the initial vector to the eigenvectors, we need [Fast Walsh–Hadamard transform](https://en.wikipedia.org/wiki/Fast_Walsh%E2%80%93Hadamard_transform).
</original>
<fixed>
We notice that the eigenvalue is only related to the number of ones in $i$, and it is not hard to calc one eigenvalue in $O(m)$ time. To decompose the initial vector to the eigenvectors, we need Fast Walsh–Hadamard transform.
</fixed>
</453_D. Little Pony and Elements of Harmony>

<865_D. Buy Low Sell High>
<original>
Let's introduce the idea of [options](https://en.wikipedia.org/wiki/Option_%28finance%29) to the problem. Instead of having to buy stock when it is at a given price, each day you gain the option to buy a share at that days price, which you can exercise at any time in the future. This way we only need to exercise an option in order to sell it, and we never need to "hold" any stock.
</original>
<fixed>
Let's introduce the idea of `options` to the problem. Instead of having to buy stock when it is at a given price, each day you gain the option to buy a share at that days price, which you can exercise at any time in the future. This way we only need to exercise an option in order to sell it, and we never need to "hold" any stock.
</fixed>
</865_D. Buy Low Sell High>

<1326_A. Bad Ugly Numbers>
<original>
[link](https://pastebin.com/KEBHMi12)
</original>
<fixed>
<remove>[link](https://pastebin.com/KEBHMi12)</remove>
</fixed>
</1326_A. Bad Ugly Numbers>

<1253_F. Cheap Robot>
<original>
[Solution 1](https://pastebin.com/xrm0MU71) 
</original>
<fixed>
<remove>[Solution 1](https://pastebin.com/xrm0MU71)</remove>
</fixed>
</1253_F. Cheap Robot>

<900_B. Position in Fraction>
<original>
In this task you should complete [long division](https://en.wikipedia.org/wiki/Long_division) and stop, when one [period](https://en.wikipedia.org/wiki/Fraction_(mathematics)) passed. Period can't be more than $b$ by [pigeonhole principle](https://en.wikipedia.org/wiki/Pigeonhole_principle). So you need to complete $b$ iterations and if $c$ digit hasn't been met, print $ - 1$.
</original>
<fixed>
In this task you should complete long division and stop, when one period passed. Period can't be more than $b$ by pigeonhole principle. So you need to complete $b$ iterations and if $c$ digit hasn't been met, print $-1$.
</fixed>
</900_B. Position in Fraction>

<865_G. Flowers and Chocolate>
<original>
Now lets consider how to compute the number of ways to make a basket with exactly $K$ chocolates. Define a polynomial $Q(x) = 1 - \sum_{i=1}^{B} x^{c_i}$. Then if we compute $x^{-K} \bmod Q(x)$, the coefficient of $x^0$ gives the number of ways to make a basket with exactly $K$ chocolates. This can be derived from a [Generating Function](https://en.wikipedia.org/wiki/Generating_function), but we will provide an alternate derivation.
</original>
<fixed>
Now lets consider how to compute the number of ways to make a basket with exactly $K$ chocolates. Define a polynomial $Q(x) = 1 - \sum_{i=1}^{B} x^{c_i}$. Then if we compute $x^{-K} \bmod Q(x)$, the coefficient of $x^0$ gives the number of ways to make a basket with exactly $K$ chocolates. This can be derived from a Generating Function, but we will provide an alternate derivation.
</fixed>
</865_G. Flowers and Chocolate>

<1242_C. Sum Balance>
<original>
This is a classical problem that can be solved in $O(3^n)$ using dynamic programming. For a subset $X$ of $\{1,\ldots,k\}$, define $dp[X]$ to be `true` if $X$ can be exactly covered, and `false` otherwise. Firstly, $dp[\varnothing] = true$. To find $dp[X]$ for $X \neq \varnothing$, iterate over all subsets $S$ of $X$, and check whether $S$ is visited by some cycle and $X \setminus S$ can be covered (e.g., $dp[X \setminus S]$ is `true`). Then the answer is $dp[\{1,\ldots,k\}]$. This algorithm can be implemented with complexity $O(3^k)$, you can read about it here:[https://cp-algorithms.com/algebra/all-submasks.html](https://cp-algorithms.com/algebra/all-submasks.html). The reordering can be restored from this DP table.
</original>
<fixed>
This is a classical problem that can be solved in $O(3^n)$ using dynamic programming. For a subset $X$ of $\{1,\ldots,k\}$, define $dp[X]$ to be `true` if $X$ can be exactly covered, and `false` otherwise. Firstly, $dp[\varnothing] = true$. To find $dp[X]$ for $X \neq \varnothing$, iterate over all subsets $S$ of $X$, and check whether $S$ is visited by some cycle and $X \setminus S$ can be covered (e.g., $dp[X \setminus S]$ is `true`). Then the answer is $dp[\{1,\ldots,k\}]$. This algorithm can be implemented with complexity $O(3^k)$, by iterating through all submasks. The reordering can be restored from this DP table.
</fixed>
</1242_C. Sum Balance>

<1139_D. Steps to One>
<original>
I recommend this [Expectation tutorial](https://brilliant.org/wiki/linearity-of-expectation/) to get more understanding of the basics.
</original>
<fixed>
We need to understand linearity of expectation to solve this problem.
</fixed>
</1139_D. Steps to One>

<1253_D. Harmonious Graph>
<original>
[Implementation](https://pastebin.com/Heb9bF7b)
</original>
<fixed>
<remove>[Implementation](https://pastebin.com/Heb9bF7b)</remove>
</fixed>
</1253_D. Harmonious Graph>

<1174_A. Ehab Fails to Be Thanos>
<original>
[https://pastebin.com/FDXTuDdZ](https://pastebin.com/FDXTuDdZ)
</original>
<fixed>
<remove>[https://pastebin.com/FDXTuDdZ](https://pastebin.com/FDXTuDdZ)</remove>
</fixed>
</1174_A. Ehab Fails to Be Thanos>

<1113_F. Sasha and Interesting Fact from Graph Theory>
<original>
[Author's solution](https://ideone.com/vbiC9L)
</original>
<fixed>
<remove>[Author's solution](https://ideone.com/vbiC9L)</remove>
</fixed>
</1113_F. Sasha and Interesting Fact from Graph Theory>

<736_D. Permutations>
<original>
This problem consists of 3 ideas. Idea 1: remainder modulo 2 of the number of permutation is equal to the remainder modulo 2 of the [determinant](https://en.wikipedia.org/wiki/Determinant) of the matrix whose entries are 1 if (ai,bi) is in our list and 0 otherwise. Idea 2: If we cahnge 1 by 0, then the determinant will differ by algebraic compliment. That is, if we count inverse matrix, than it will reflect reminders modulo 2 (B(m,n)=A'(m,n)/detA, detA is odd). Idea 3: Inverse matrix can be counted for O((n/32)^3) time. However, we can work is field of integers modulo 2. The summation can be replaced by XOR. So if we store in one "int" not a single but 32 numbers, then we can reduce our assymptocy to O(n^3/32), which is OK.
</original>
<fixed>
This problem consists of 3 ideas. Idea 1: remainder modulo 2 of the number of permutation is equal to the remainder modulo 2 of the determinant of the matrix whose entries are 1 if (ai,bi) is in our list and 0 otherwise. Idea 2: If we cahnge 1 by 0, then the determinant will differ by algebraic compliment. That is, if we count inverse matrix, than it will reflect reminders modulo 2 (B(m,n)=A'(m,n)/detA, detA is odd). Idea 3: Inverse matrix can be counted for O((n/32)^3) time. However, we can work is field of integers modulo 2. The summation can be replaced by XOR. So if we store in one "int" not a single but 32 numbers, then we can reduce our assymptocy to O(n^3/32), which is OK.
</fixed>
</736_D. Permutations>

<245_B. Internet Address>
<original>
Problem guarantees that there exists an Internet resource address from which we can obtain our input. At first, let's find **Protocol**  of address. It's sufficient to only check first letter of input, if it's $h$ then protocol is $http$ otherwise, it's $ftp$. Now, let's find position of $.ru$. We can iterate over our string from right to left and greedily choose the first occurrence of $.ru$ as [TLD](https://en.wikipedia.org/wiki/Top-level_domain). Now the rest of Internet address can be obtained easily as we have positions of **Protocol**  and **TLD** . Just note that we should check whether $ < context > $ is present after $.ru$ or not. Also picking $.ru$ greedily from left to right fails following testcase, hence it's incorrect.
</original>
<fixed>
Problem guarantees that there exists an Internet resource address from which we can obtain our input. At first, let's find **Protocol**  of address. It's sufficient to only check first letter of input, if it's $h$ then protocol is $http$ otherwise, it's $ftp$. Now, let's find position of $.ru$. We can iterate over our string from right to left and greedily choose the first occurrence of $.ru$ as `Top level domain`. Now the rest of Internet address can be obtained easily as we have positions of **Protocol**  and **TLD** . Just note that we should check whether $ < context > $ is present after $.ru$ or not. Also picking $.ru$ greedily from left to right fails following testcase, hence it's incorrect.
</fixed>
</245_B. Internet Address>

<1290_E. Cartesian Tree >
<original>
Check part 2 of [this blog](https://codeforces.com/blog/entry/57319) and [this proof of time complexity](https://codeforces.com/blog/entry/57319?#comment-409924).
</original>
<fixed>
<remove>Check part 2 of [this blog](https://codeforces.com/blog/entry/57319) and [this proof of time complexity](https://codeforces.com/blog/entry/57319?#comment-409924).</remove>
</fixed>
</1290_E. Cartesian Tree >

<160_D. Edges in MST>
<original>
What's left is to get all of V quickly. Maybe you hear about Tarjan before, he invented an algorithm based on DFS to get all bridges in an edge-undirected graph in O(|V|+|E|). Read this page on Wikipedia for detailed information: [Bridge](https://en.wikipedia.org/wiki/Bridge_%28graph_theory%29).
</original>
<fixed>
What's left is to get all of V quickly. Maybe you hear about Tarjan before, he invented an algorithm based on DFS to get all bridges in an edge-undirected graph in O(|V|+|E|).
</fixed>
</160_D. Edges in MST>

<226_C. Anniversary>
<original>
Now you are to notice an analogy with [Euclidean algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm) and to understand, that we've got necessary equality for $GCD$ of two Fibonacci numbers.
</original>
<fixed>
Now you are to notice an analogy with Euclidean algorithm and to understand, that we've got necessary equality for $GCD$ of two Fibonacci numbers.
</fixed>
</226_C. Anniversary>

<346_D. Robot Control>
<original>
In fact, we add a part of targeted datas in pretest, these datas are enough to block most of our [Bellman-Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm), although there is still a few participator can get accepted by Bellman-Ford algorithm during the contest.
</original>
<fixed>
In fact, we add a part of targeted datas in pretest, these datas are enough to block most of our Bellman-Ford algorithm, although there is still a few participator can get accepted by Bellman-Ford algorithm during the contest.
</fixed>
</346_D. Robot Control>

<477_E. Dreamoon and Notepad>
<original>
sample code: [8212528](/contest/477/submission/8212528)
</original>
<fixed>
<remove>[8212528](/contest/477/submission/8212528)</remove>
</fixed>
</477_E. Dreamoon and Notepad>

<123_A. Prime Permutation>
<original>
[The author's solution](/contest/123/submission/835585)
</original>
<fixed>
<remove>[The author's solution](/contest/123/submission/835585)</remove>
</fixed>
</123_A. Prime Permutation>

<665_E. Beautiful Subarrays>
<original>
Let $s_i$ be the xor of the first $i$ elements on the prefix of $a$. Then the interval $(i, j]$ is beautiful if $s_j \oplus s_i \geq k$. Let's iterate over $j$ from $1$ to $n$ and consider the values $s_j$ as the binary strings. On each iteration we should increase the answer by the value $z_j$ — the number of numbers $s_i$ ($i < j$) so $s_j \oplus s_i \geq k$. To do that we can use the [trie](https://ru.wikipedia.org/wiki/Trie) data structure. Let's store in the trie all the values $s_i$ for $i < j$. Besides the structure of the trie we should also store in each vertex the number of leaves in the subtree of that vertex (it can be easily done during adding of each binary string). To calculate the value $z_j$ let's go down by the trie from the root. Let's accumulate the value $cur$ equals to the xor of the prefix of the value $s_j$ with the already passed in the trie path. Let the current bit in $s_j$ be equal to $b$ and $i$ be the depth of the current vertex in the trie. If the number $cur + 2^i ≥ k$ then we can increase $z_j$ by the number of leaves in vertex $n t_{v, b \oplus 1}$, because all the leaves in the subtree of tha vertex correspond to the values $s_i$ that for sure gives $s_j \oplus s_i \geq k$. After that we should go down in the subtree $b$. Otherwise if $cur + 2^i < k$ then we should simply go down to the subtree $b \oplus 1$ and recalculate the value $cur = cur + 2^i$.
</original>
<fixed>
Let $s_i$ be the xor of the first $i$ elements on the prefix of $a$. Then the interval $(i, j]$ is beautiful if $s_j \oplus s_i \geq k$. Let's iterate over $j$ from $1$ to $n$ and consider the values $s_j$ as the binary strings. On each iteration we should increase the answer by the value $z_j$ — the number of numbers $s_i$ ($i < j$) so $s_j \oplus s_i \geq k$. To do that we can use the trie data structure. Let's store in the trie all the values $s_i$ for $i < j$. Besides the structure of the trie we should also store in each vertex the number of leaves in the subtree of that vertex (it can be easily done during adding of each binary string). To calculate the value $z_j$ let's go down by the trie from the root. Let's accumulate the value $cur$ equals to the xor of the prefix of the value $s_j$ with the already passed in the trie path. Let the current bit in $s_j$ be equal to $b$ and $i$ be the depth of the current vertex in the trie. If the number $cur + 2^i ≥ k$ then we can increase $z_j$ by the number of leaves in vertex $n t_{v, b \oplus 1}$, because all the leaves in the subtree of tha vertex correspond to the values $s_i$ that for sure gives $s_j \oplus s_i \geq k$. After that we should go down in the subtree $b$. Otherwise if $cur + 2^i < k$ then we should simply go down to the subtree $b \oplus 1$ and recalculate the value $cur = cur + 2^i$.
</fixed>
</665_E. Beautiful Subarrays>

<338_D. GCD Table>
<original>
According to [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem), such a system has a solution iff for each pair of indices `x, y (0 <= x, y <= k-1)` we have `-x = -y (mod GCD(a[x+1], a[y+1]))`. Let's denote `L = LCM(a[1], ..., a[k])`. If the system has a solution, then it is singular on interval `[0, L)` and all the other solutions are congruent to it modulo `L`. Suppose that we have found the minimum non-negative `j` which satisfies the given system. Then, if `a` occurs in `G`, it will start from the `j`-th element of the `i`-th row. Theoretically, it may begin at any index of form `j+x*L, x>=0`, but since `i = L`, we have `G(i, j+X*L) = GCD(i, j+X*i) = GCD(i, j)`. So it is sufficient to check whether the `k` consecutive elements which begin at index `j` in row `i` coincide with sequence `a`. It is also clear that when `j > m-k+1`, the answer is `NO`.
</original>
<fixed>
According to Chinese Remainder Theorem, such a system has a solution iff for each pair of indices `x, y (0 <= x, y <= k-1)` we have `-x = -y (mod GCD(a[x+1], a[y+1]))`. Let's denote `L = LCM(a[1], ..., a[k])`. If the system has a solution, then it is singular on interval `[0, L)` and all the other solutions are congruent to it modulo `L`. Suppose that we have found the minimum non-negative `j` which satisfies the given system. Then, if `a` occurs in `G`, it will start from the `j`-th element of the `i`-th row. Theoretically, it may begin at any index of form `j+x*L, x>=0`, but since `i = L`, we have `G(i, j+X*L) = GCD(i, j+X*i) = GCD(i, j)`. So it is sufficient to check whether the `k` consecutive elements which begin at index `j` in row `i` coincide with sequence `a`. It is also clear that when `j > m-k+1`, the answer is `NO`.
</fixed>
</338_D. GCD Table>

<1293_F. Chaotic V.>
<original>
It's proven that $f(k) = M + \log{\log{k}}$, with $M$ being the [Meissel-Mertens constant](https://en.wikipedia.org/wiki/Meissel-Mertens_constant).
</original>
<fixed>
It's proven that $f(k) = M + \log{\log{k}}$, with $M$ being the Meissel-Mertens constant.
</fixed>
</1293_F. Chaotic V.>

<332_E. Binary Key>
<original>
[Code](http://pastebin.com/zPmfJJdV)
</original>
<fixed>
<remove>[Code](http://pastebin.com/zPmfJJdV)</remove>
</fixed>
</332_E. Binary Key>

<477_A. Dreamoon and Sums>
<original>
sample code: [8215188](/contest/476/submission/8215188)
</original>
<fixed>
<remove>[8215188](/contest/476/submission/8215188)</remove>
</fixed>
</477_A. Dreamoon and Sums>

<932_G. Palindrome Partition>
<original>
As discussed in this [blog](//codeforces.com/blog/entry/19193), we can use an eertree to implement the solution. On the other hand, we can avoid the use of any suffix structure by following the algorithm described in this [paper](https://arxiv.org/pdf/1403.2431.pdf).
</original>
<fixed>
We can use an eertree to implement the solution.
</fixed>
</932_G. Palindrome Partition>

<585_F. Digits of Number Pi>
<original>
Consider all substrings of string $s$ with length $\lfloor d/2 \rfloor$. Let's add them all to [trie](https://en.wikipedia.org/wiki/Trie) data structure, calculate failure links and build automata by digits. We can do that in linear time using [Aho-Korasik](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm) algorithm. Now to solve the problem we should calculate dp $z_{i, v, b_1, b_2, b}$. State of dp is described by five numbers: $i$ — number of digits, that we already put to our number, $v$ — in which vertex of trie we are, $b_1$ — equals to one if the prefix that we built is equals to prefix of $x$, $b_2$ — equals to one if the prefix that we built is equals to prefix of $y$, $b$ — equals to one if we already have some substring with length $\lfloor d/2 \rfloor$ on the prexif that we built. The value of dp is the number of ways to built prefix with the given set of properties. To update dp we should iterate over the digit that we want to add to prefix, check that we still is in segment $[x, y]$, go from vertex $v$ to the next vertex in automata. So the answer is the sum by all $v, b_1, b_2$ $z_{b, v, v_1, v_2, 1}$.
</original>
<fixed>
Consider all substrings of string $s$ with length $\lfloor d/2 \rfloor$. Let's add them all to trie data structure, calculate failure links and build automata by digits. We can do that in linear time using Aho-Corasick algorithm. Now to solve the problem we should calculate dp $z_{i, v, b_1, b_2, b}$. State of dp is described by five numbers: $i$ — number of digits, that we already put to our number, $v$ — in which vertex of trie we are, $b_1$ — equals to one if the prefix that we built is equals to prefix of $x$, $b_2$ — equals to one if the prefix that we built is equals to prefix of $y$, $b$ — equals to one if we already have some substring with length $\lfloor d/2 \rfloor$ on the prexif that we built. The value of dp is the number of ways to built prefix with the given set of properties. To update dp we should iterate over the digit that we want to add to prefix, check that we still is in segment $[x, y]$, go from vertex $v$ to the next vertex in automata. So the answer is the sum by all $v, b_1, b_2$ $z_{b, v, v_1, v_2, 1}$.
</fixed>
</585_F. Digits of Number Pi>

<300_E. Empire Strikes Back>
<original>
[Аuthor's solution](http://pastebin.com/71vYY41X)
</original>
<fixed>
<remove>[Аuthor's solution](http://pastebin.com/71vYY41X)</remove>
</fixed>
</300_E. Empire Strikes Back>

<384_D. Volcanoes>
<original>
Code: [http://pastie.org/8651817](http://pastie.org/8651817)
</original>
<fixed>
<remove>[http://pastie.org/8651817](http://pastie.org/8651817)</remove>
</fixed>
</384_D. Volcanoes>

<477_D. Dreamoon and Binary>
<original>
sample code: [8215216](/contest/477/submission/8215216)
</original>
<fixed>
<remove>[8215216](/contest/477/submission/8215216)</remove>
</fixed>
</477_D. Dreamoon and Binary>

<725_F. Family Photos>
<original>
[code](//codeforces.com/contest/725/submission/21731928)
</original>
<fixed>
<remove>[code](//codeforces.com/contest/725/submission/21731928)</remove>
</fixed>
</725_F. Family Photos>

<865_E. Hex Dyslexia>
<original>
First, observe that for a solution to exist, the sum of the digits in the input must be divisible by 15. This is because of the [Casting out Nines](https://en.wikipedia.org/wiki/Casting_out_nines) rule, but applied in base 16. Furthermore, the sum of digits, when divided by 15, tells us how many carries must be performed when adding the answer to the input. We can try every possible set of positions for the carries, of which there are at most ${13 \choose 6} = 1716$ ways. Once the carries are fixed, for each position we know the exact difference between the original digit in that position and the permuted digit in that position.
</original>
<fixed>
First, observe that for a solution to exist, the sum of the digits in the input must be divisible by 15. This is because of the Casting out Nines rule, but applied in base 16. Furthermore, the sum of digits, when divided by 15, tells us how many carries must be performed when adding the answer to the input. We can try every possible set of positions for the carries, of which there are at most ${13 \choose 6} = 1716$ ways. Once the carries are fixed, for each position we know the exact difference between the original digit in that position and the permuted digit in that position.
</fixed>
</865_E. Hex Dyslexia>

<373_E. Watching Fireworks is Fun>
<original>
Intended solution uses sliding window maximum (see this page [sliding window](http://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html) for some information), since the interval $[j — t * d, j + t * d]$ is independent for all the fireworks. It can be implemented by simple array or deque. This will speed up to calculate formula, and overall complexity will be $O(m n)$.
</original>
<fixed>
Intended solution uses sliding window maximum, since the interval $[j — t * d, j + t * d]$ is independent for all the fireworks. It can be implemented by simple array or deque. This will speed up to calculate formula, and overall complexity will be $O(m n)$.
</fixed>
</373_E. Watching Fireworks is Fun>

<609_E. Minimum spanning tree for each edge>
<original>
Let's build any [MST](https://en.wikipedia.org/wiki/Minimum_spanning_tree) with any fast algorithm (for example with [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)). For all edges in MST the answer is the weight of the MST. Let's consider any other edge $(x, y)$. There is exactly one path between $x$ and $y$ in the MST. Let's remove mostly heavy edge on this path and add edge $(x, y)$. Resulting tree is the MST contaning edge $(x, y)$ (this can be proven by Tarjan criterion).
</original>
<fixed>
Let's build any Minimum Spanning Tree (MST) with any fast algorithm (for example with Kruskal's algorithm). For all edges in MST the answer is the weight of the MST. Let's consider any other edge $(x, y)$. There is exactly one path between $x$ and $y$ in the MST. Let's remove mostly heavy edge on this path and add edge $(x, y)$. Resulting tree is the MST contaning edge $(x, y)$ (this can be proven by Tarjan criterion).
</fixed>
</609_E. Minimum spanning tree for each edge>

<991_E. Bus Number>
<original>
Now for each subset of digits we have to calculate amount of corresponding correct bus numbers. It can be calculated in $O(k)$ operations using permutations of multisets formula (see `Permutations of multisets` at the article about [permutations](https://en.wikipedia.org/wiki/Permutation#Permutations_of_multisets) and [multinomial coefficients](https://en.wikipedia.org/wiki/Multinomial_theorem))
</original>
<fixed>
Now for each subset of digits we have to calculate amount of corresponding correct bus numbers. It can be calculated in $O(k)$ operations using permutations of multisets formula.
</fixed>
</991_E. Bus Number>

<981_H. K Paths>
<original>
[Solution in $O(n log^2 n)$](https://pastebin.com/0h3SYJJm)
</original>
<fixed>
<remove>[Solution in $O(n log^2 n)$](https://pastebin.com/0h3SYJJm)</remove>
</fixed>
</981_H. K Paths>

<1168_E. Xor Permutations>
<original>
[solution](https://pastebin.com/S310JdDa)
</original>
<fixed>
<remove>[solution](https://pastebin.com/S310JdDa)</remove>
</fixed>
</1168_E. Xor Permutations>

<123_B. Squares>
<original>
[The author's solution](/contest/123/submission/835587)
</original>
<fixed>
<remove>[The author's solution](/contest/123/submission/835587)</remove>
</fixed>
</123_B. Squares>

<991_A. If at first you don't succeed...>
<original>
In general you are recommended to view [inclusion–exclusion principle](https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle).
</original>
<fixed>
<remove>In general you are recommended to view [inclusion–exclusion principle](https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle).</remove>
</fixed>
</991_A. If at first you don't succeed...>

<340_E. Iahub and Permutations>
<original>
We can compute binomial coefficients using Pascal's triangle. Using inclusion and exclusion principle, we get *O*(*N*^2). Please note that there exist an *O*(*N*) solution for this task, using inclusion and exclusion principle, but it's not necessary to get AC. I'll upload [Gerald](/profile/Gerald)'s source [here](http://pastie.org/8287332).
</original>
<fixed>
We can compute binomial coefficients using Pascal's triangle. Using inclusion and exclusion principle, we get *O*(*N*^2). Please note that there exist an *O*(*N*) solution for this task, using inclusion and exclusion principle, but it's not necessary to get AC.
</fixed>
</340_E. Iahub and Permutations>

<559_B. Equivalent Strings>
<original>
Let us note that "equivalence" described in the statements is actually [equivalence relation](https://en.wikipedia.org/wiki/Equivalence_relation), it is reflexively, simmetrically and transitive. It is meant that set of all string is splits to equivalence classes. Let's find lexicographic minimal strings what is equivalent to first and to second given string. And then check if its are equals.
</original>
<fixed>
Let us note that "equivalence" described in the statements is actually `equivalence relation`, it is reflexively, simmetrically and transitive. It is meant that set of all string is splits to equivalence classes. Let's find lexicographic minimal strings what is equivalent to first and to second given string. And then check if its are equals.
</fixed>
</559_B. Equivalent Strings>

<975_C. Valhalla Siege>
<original>
[Solution](https://pastebin.com/fcbXrqy4)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/fcbXrqy4)</remove>
</fixed>
</975_C. Valhalla Siege>

<487_B. Strip>
<original>
For more details about monotonic queue, you can see [here](http://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html)
</original>
<fixed>
<remove>For more details about monotonic queue, you can see [here](http://people.cs.uct.ac.za/~ksmith/articles/sliding_window_minimum.html)</remove>
</fixed>
</487_B. Strip>

<887_D. Ratings and Reality Shows>
<original>
[Solution](https://pastebin.com/te2R75QA)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/te2R75QA)</remove>
</fixed>
</887_D. Ratings and Reality Shows>

<681_C. Heap Operations>
<original>
[Code](https://ideone.com/1iyHy8)
</original>
<fixed>
<remove>[Code](https://ideone.com/1iyHy8)</remove>
</fixed>
</681_C. Heap Operations>

<736_B. Taxes>
<original>
The first obvious fact is that the answer for prime numbers is 1. If the number is not prime, then the answer is at least 2. When is it possible? It is possible in 2 cases; when it is sum of 2 primes of its maximal divisor is 2. If 2 divides n, then so does integer n/2. n/2<=2=>n<=4=>n=4, where n is prime. According to [Goldbach's conjecture](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture), which is checked for all numbers no more than 10^9, every number is a sum of two prime numbers. Odd number can be sum of two primes, if (n-2) is prime (the only even prime number is 2). Otherwise, the answer is 3 — n=3+(n-3), (n-3) is sum of 2 primes, because it is even.
</original>
<fixed>
The first obvious fact is that the answer for prime numbers is 1. If the number is not prime, then the answer is at least 2. When is it possible? It is possible in 2 cases; when it is sum of 2 primes of its maximal divisor is 2. If 2 divides n, then so does integer n/2. n/2<=2=>n<=4=>n=4, where n is prime. According to Goldbach's conjecture, which is checked for all numbers no more than 10^9, every number is a sum of two prime numbers. Odd number can be sum of two primes, if (n-2) is prime (the only even prime number is 2). Otherwise, the answer is 3 — n=3+(n-3), (n-3) is sum of 2 primes, because it is even.
</fixed>
</736_B. Taxes>

<1055_G. Jellyfish Nightmare>
<original>
First of all, we will solve a simpler problem: you need to check if it is possible for Bob to swim along the whole lane without any jellyfish stinging him. The position of Bob is identified by the location of his first vertex. Let's find out what are the prohibited areas for it. If a jellyfish had no activity zone and would only sting Bob only if he was swimming over it, the prohibited areas would look like polygons around every jellyfish. If we add the activity zone of radius $r$, prohibited areas will become "inflated" polygons. To be more precise, if the shape of Bob is a polygon $P$ they would have a shape of [Minkowski sum](https://en.wikipedia.org/wiki/Minkowski_addition) of a polygon $-P$ with a circle of radius $r$. $-P$ here stands for the polygon inverted relative to the origin.
</original>
<fixed>
First of all, we will solve a simpler problem: you need to check if it is possible for Bob to swim along the whole lane without any jellyfish stinging him. The position of Bob is identified by the location of his first vertex. Let's find out what are the prohibited areas for it. If a jellyfish had no activity zone and would only sting Bob only if he was swimming over it, the prohibited areas would look like polygons around every jellyfish. If we add the activity zone of radius $r$, prohibited areas will become "inflated" polygons. To be more precise, if the shape of Bob is a polygon $P$ they would have a shape of Minkowski sum of a polygon $-P$ with a circle of radius $r$. $-P$ here stands for the polygon inverted relative to the origin.
</fixed>
</1055_G. Jellyfish Nightmare>

<618_A. Slime Combining>
<original>
[simulation](//codeforces.com/contest/618/submission/15669470)
</original>
<fixed>
<remove>[simulation](//codeforces.com/contest/618/submission/15669470)</remove>
</fixed>
</618_A. Slime Combining>

<736_E. Chess Championship>
<original>
Suppose set (a1,a2,...,am). Then the list is valid if set {2m-2, 2m-4, 2m-6, ..., 0} [majorizes](https://en.wikipedia.org/wiki/Majorization) the set {a1,a2,...,am}. Let us prove it! Part 1: Suppose n<=m. Top n players will play n(n-1)/2 games with each other and n(m-n) games with low-ranked contestants. In these games they will collect 2*n(n-1)/2 points (in each game there is exactly 2 points) for sure and at most 2*n*(m-n) points in games with others. So they will have at most 2*(n*(n-1)/2+n*(m-n))=2*((m-1)+(m-2)+...+(m-n)) points. Now construction: Let's construct results of participant with most points and then use recursion. Suppose the winner has even number of points (2*(m-n) for some n). Then we consider that he lost against contestants holding 2,3,4,...,n places and won against others. If champion had odd number of points (2*(m-n)-1 for some n), then we will construct the same results supposing that he draw with (n+1)th player instead of winning agianst him. It is easy to check that majorization is invariant, so in the end we will have to deal with 1 men competition, when set of scores {a1} is majorized by set {0}. So a1=0, and there is obvious construction for this case. So we have such an algorithm: we search for a compiment set which is majorized by {2m-2,2m-4,...,0}. If there is no such set answer is NO. Otherwise answer is YES and we construct our table as shown above. Assymptosy is O(m^2logm) (calling recursion m times, sorting the array (we can lose non-decreasing order because of poor results) and then passing on it linearly).
</original>
<fixed>
Suppose set (a1,a2,...,am). Then the list is valid if set {2m-2, 2m-4, 2m-6, ..., 0} majorizes the set {a1,a2,...,am}. Let us prove it! Part 1: Suppose n<=m. Top n players will play n(n-1)/2 games with each other and n(m-n) games with low-ranked contestants. In these games they will collect 2*n(n-1)/2 points (in each game there is exactly 2 points) for sure and at most 2*n*(m-n) points in games with others. So they will have at most 2*(n*(n-1)/2+n*(m-n))=2*((m-1)+(m-2)+...+(m-n)) points. Now construction: Let's construct results of participant with most points and then use recursion. Suppose the winner has even number of points (2*(m-n) for some n). Then we consider that he lost against contestants holding 2,3,4,...,n places and won against others. If champion had odd number of points (2*(m-n)-1 for some n), then we will construct the same results supposing that he draw with (n+1)th player instead of winning agianst him. It is easy to check that majorization is invariant, so in the end we will have to deal with 1 men competition, when set of scores {a1} is majorized by set {0}. So a1=0, and there is obvious construction for this case. So we have such an algorithm: we search for a compiment set which is majorized by {2m-2,2m-4,...,0}. If there is no such set answer is NO. Otherwise answer is YES and we construct our table as shown above. Assymptosy is O(m^2logm) (calling recursion m times, sorting the array (we can lose non-decreasing order because of poor results) and then passing on it linearly).
</fixed>
</736_E. Chess Championship>

<340_C. Tourist Problem>
<original>
Official solution: [4383420](/contest/340/submission/4383420)
</original>
<fixed>
<remove>[4383420](/contest/340/submission/4383420)</remove>
</fixed>
</340_C. Tourist Problem>

<946_G. Almost Increasing Array>
<original>
[https://pastebin.com/BiaFgYx6](https://pastebin.com/BiaFgYx6)
</original>
<fixed>
<remove>[https://pastebin.com/BiaFgYx6](https://pastebin.com/BiaFgYx6)</remove>
</fixed>
</946_G. Almost Increasing Array>

<975_B. Mancala>
<original>
[Solution](https://pastebin.com/zdD4NtdF)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/zdD4NtdF)</remove>
</fixed>
</975_B. Mancala>

<95_E. Lucky Country>
<original>
Let all C[i] = (2^k)-1, i. e. C[i] = 1 + 2 + 4 + 8 + … + 2^(k-1). Obviously, that if chose some subset of this powers we can get any number from 0 to C[i], inclusive. So, the problem now is next: For each A[i] is log(C[i]) things (cost of this thing is size of subset that create it), each can be used at most once. This is standard “Knapsack” problem (read [this](https://en.wikipedia.org/wiki/Knapsack_problem)). Complexity of this algorithm is O(N * S), when S is the sum for all log(C[i]). If C[i] is not power of 2, then we must find maximal k, which (2^k)-1 <= C[i] and add C[i]-((2^k)-1) to set.
</original>
<fixed>
Let all C[i] = (2^k)-1, i. e. C[i] = 1 + 2 + 4 + 8 + … + 2^(k-1). Obviously, that if chose some subset of this powers we can get any number from 0 to C[i], inclusive. So, the problem now is next: For each A[i] is log(C[i]) things (cost of this thing is size of subset that create it), each can be used at most once. This is standard “Knapsack” problem. Complexity of this algorithm is O(N * S), when S is the sum for all log(C[i]). If C[i] is not power of 2, then we must find maximal k, which (2^k)-1 <= C[i] and add C[i]-((2^k)-1) to set.
</fixed>
</95_E. Lucky Country>

<384_C. Milking cows>
<original>
Code: [http://pastie.org/8651813](http://pastie.org/8651813)
</original>
<fixed>
<remove>[http://pastie.org/8651813](http://pastie.org/8651813)</remove>
</fixed>
</384_C. Milking cows>

<332_B. Maximum Absurdity>
<original>
[Code](http://pastebin.com/FJrik8jC)
</original>
<fixed>
<remove>[Code](http://pastebin.com/FJrik8jC)</remove>
</fixed>
</332_B. Maximum Absurdity>

<123_E. Maze>
<original>
[The author's solution](/contest/123/submission/835592)
</original>
<fixed>
<remove>[The author's solution](/contest/123/submission/835592)</remove>
</fixed>
</123_E. Maze>

<887_C. Solution for Cube>
<original>
[First solution](https://pastebin.com/G8kAaSVz)
</original>
<fixed>
<remove>[First solution](https://pastebin.com/G8kAaSVz)</remove>
</fixed>
</887_C. Solution for Cube>

<336_A. Vasily the Bear and Triangle>
<original>
[Author's solution](http://pastebin.com/fNz05bHS)
</original>
<fixed>
<remove>[Author's solution](http://pastebin.com/fNz05bHS)</remove>
</fixed>
</336_A. Vasily the Bear and Triangle>

<226_A. Flying Saucer Segments>
<original>
And, in conclusion, notice that the task is equal to [Hanoi Towers](https://en.wikipedia.org/wiki/Hanoi_tower) problem with a slight modification (it's impossible to move disks between one pair of rods).
</original>
<fixed>
And, in conclusion, notice that the task is equal to Hanoi Towers problem with a slight modification (it's impossible to move disks between one pair of rods).
</fixed>
</226_A. Flying Saucer Segments>

<332_D. Theft of Blueprints>
<original>
[Code](http://pastebin.com/cdmkTAxA)
</original>
<fixed>
<remove>[Code](http://pastebin.com/cdmkTAxA)</remove>
</fixed>
</332_D. Theft of Blueprints>

<340_B. Maximal Area Quadrilateral>
<original>
![ ](https://imageshack.us/a/img42/9976/dwkn.png)
</original>
<fixed>
<remove>![ ](https://imageshack.us/a/img42/9976/dwkn.png)</remove>
</fixed>
</340_B. Maximal Area Quadrilateral>

<1305_G. Kuroni and Antihype>
<original>
For each mask, find two largest present weights (from different components) which are submasks of this mask in $O(2^{18} \cdot 18)$ with [SOS DP](https://codeforces.com/blog/entry/45223). Then, for each component we can find the edge from this component to some other component with the largest weight, and do one iteration of Boruvka. Complexity $O(2^{18} \cdot 18 \cdot log(n))$.
</original>
<fixed>
For each mask, find two largest present weights (from different components) which are submasks of this mask in $O(2^{18} \cdot 18)$ with Sum over Subsets Dynamic Programming (SOS DP). Then, for each component we can find the edge from this component to some other component with the largest weight, and do one iteration of Boruvka. Complexity $O(2^{18} \cdot 18 \cdot log(n))$.
</fixed>
</1305_G. Kuroni and Antihype>

<887_F. Row of Models>
<original>
[Solution](https://pastebin.com/eM5MCtbZ)
</original>
<fixed>
<remove>[Solution](https://pastebin.com/eM5MCtbZ)</remove>
</fixed>
</887_F. Row of Models>

<300_C. Beautiful Numbers>
<original>
[Аuthor's solution](http://pastebin.com/XwP7MmEa)
</original>
<fixed>
<remove>[Аuthor's solution](http://pastebin.com/XwP7MmEa)</remove>
</fixed>
</300_C. Beautiful Numbers>

<1113_B. Sasha and Magnetic Machines>
<original>
[Author's solution](https://ideone.com/mkondU)
</original>
<fixed>
<remove>[Author's solution](https://ideone.com/mkondU)</remove>
</fixed>
</1113_B. Sasha and Magnetic Machines>

