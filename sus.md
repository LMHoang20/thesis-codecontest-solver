Given a competitve programming problem, its editorial, and a code solution, the task is to explain step by step what the code is doing

# Problem

You are given an array of integers 𝑎1,𝑎2,…,𝑎𝑛. You can perform the following operation any number of times (possibly zero):Choose any element 𝑎𝑖 from the array and change its value to any integer between 0 and 𝑎𝑖 (inclusive). More formally, if 𝑎𝑖<0, replace 𝑎𝑖 with any integer in [𝑎𝑖,0], otherwise replace 𝑎𝑖 with any integer in [0,𝑎𝑖].Let 𝑟 be the minimum possible product of all the 𝑎𝑖 after performing the operation any number of times.Find the minimum number of operations required to make the product equal to 𝑟. Also, print one such shortest sequence of operations. If there are multiple answers, you can print any of them.InputEach test consists of multiple test cases. The first line contains a single integer 𝑡 (1≤𝑡≤500) - the number of test cases. This is followed by their description.The first line of each test case contains the a single integer 𝑛 (1≤𝑛≤100) — the length of the array.The second line of each test case contains 𝑛 integers 𝑎1,𝑎2,…,𝑎𝑛 (−109≤𝑎𝑖≤109).OutputFor each test case:The first line must contain the minimum number of operations 𝑘 (0≤𝑘≤𝑛).The 𝑗-th of the next 𝑘 lines must contain two integers 𝑖 and 𝑥, which represent the 𝑗-th operation. That operation consists in replacing 𝑎𝑖 with 𝑥.

Example

input:
4
1
155
4
2 8 -1 3
4
-1 0 -2 -5
4
-15 -75 -25 -30

output 
1
1 0
0
0
1
3 0

Note
In the first test case, we can change the value of the first integer into 0 and the product will become 0, which is the minimum possible.In the second test case, initially, the product of integers is equal to 2⋅8⋅(−1)⋅3=−48 which is the minimum possible, so we should do nothing in this case.

# Editorial

First, let's find the minimum product we can get. If one of the numbers is or becomes 0, then the product will be 0. Otherwise, all the numbers don't change their sign during the operation. So the initial product won't change its sign as well. Also, we can note that the absolute value will not increase after an operation. That means if the initial product is negative, we cannot decrease it. In this case the necessary number of operations will be 0.

If the initial product is positive, then we know the product won't become negative, therefore we will make it zero with 1 operation, which will be the answer and the operation will be changing any number to 0. If the initial product is zero, then we don't need to change anything, so the number of operations needed is 0.

# Code

```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

const int N = 105;

int t, n;
int a[N];

int main() {
    cin >> t;
    
    while (t--) {
        cin >> n;
        
        int c_neg = 0;
        int c_zero = 0;
        int c_pos = 0;
        
        for (int i = 1; i <= n; i++) {
            cin >> a[i];
            
            if (a[i] < 0) {
                c_neg++;
            } else if (a[i] == 0) {
                c_zero++;
            } else {
                c_pos++;
            }
        }
        
        if (c_zero || c_neg % 2) {
            cout << 0 << endl;
        } else {
            cout << 1 << endl;
            cout << 1 << " " << 0 << endl;
        }
    }
    return 0;
}
```