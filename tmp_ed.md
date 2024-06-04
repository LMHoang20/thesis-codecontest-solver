WLOG (Without loss of generality), we may assume that 0 < a_1 < a_2 <...< a_n, and a_{i+n} = -a_i for each 1 ≤ i ≤ n.
Let's sort array d firstly.
It can be observed that the array d satisfied the following property:
-  d_{2i-1}=d_{2i} for each 1 ≤ i ≤ n;
-  d_{2i}≠d_{2i+2} for each 1 ≤ i < n.
-  d_{2i} must be generated for index i or i+n.
More importantly, we have the following relation: d_{2n}-d_{2n-2}=\sum_{i=1}^{n} (a_n-a_i)+\sum_{i=1}^n (a_n+a_i) - \sum_{i=1}^n|a_{n-1}-a_i| - \sum_{i=1}^n (a_{n-1}+a_i) = (2n-2)(a_n-a_{n-1}) and observe that |a_i-a_n|+|a_i+a_n|=2a_n is a constant independent of index 1 ≤ i ≤ n.
Therefore, we may remove a_n and -a_n by subtracting some constant for d_i for all 1 ≤ i ≤ 2(n-1), indicating that we will calculate a_{i+1}-a_{i} for all 1 ≤ i < n, which can be done in O(n).
Lastly, we should determine if there exists an positive integer a_1 which generates d_1, which can be done in O(n).