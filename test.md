**Premise**:
- Nikita had a word consisting of exactly 3 lowercase Latin letters.
- The letters in the Latin alphabet are numbered from 1 to 26, where the letter "a" has the index 1, and the letter "z" has the index 26.
- He encoded this word as the sum of the positions of all the characters in the alphabet.
- However, this encoding turned out to be ambiguous
- Determine the lexicographically smallest word of 3 letters that could have been encoded.
- A string 𝑎 is lexicographically smaller than a string 𝑏 if and only if one of the following holds:
    - 𝑎 is a prefix of 𝑏, but 𝑎≠𝑏;
    - in the first position where 𝑎 and 𝑏 differ, the string 𝑎 has a letter that appears earlier in the alphabet than the corresponding letter in 𝑏.
- The first line of the input contains a single integer 𝑡 (1≤𝑡≤100) — the number of test cases in the test.
- This is followed by the descriptions of the test cases.
    - The first and only line of each test case contains an integer 𝑛 (3≤𝑛≤78) — the encoded word.
- For each test case, output the lexicographically smallest three-letter word that could have been encoded on a separate line.

**Example**

Test case 1:
```
1
24
```
```
aav
```
Test case 2:
```
1
70
```
```
rzz
```
Test case 3:
```
1
3
```
```
aaa
```
Test case 4:
```
1
55
```
```
czz
```
Test case 5:
```
1
48
```
```
auz
```

**Steps**

- input `t`
- loop through `t`
    - input `n`


**Code**
```cpp
#include<bits/stdc++.h>
using namespace std;

void solve(){
    cout << "input 2: none" << '\n';
    int n, sz = 26;
    cin >> n;
    cout << "output 2: " << n << '\n';
    string mins = "zzz", cur;
    cout << 
    for(int i = 0; i < sz; i++){
        for(int j = 0; j < sz; j++){
            for(int k = 0; k < sz; k++){
                if(i + j + k + 3 == n){
                    cur += char(i + 'a');
                    cur += char(j + 'a');
                    cur += char(k + 'a');
                    mins = cur;
                    break;
                }
            }
        }
    }
    cout << mins << "\n";
 
}
int main(){
    int t;
    cin >> t;
    while(t--) {
        solve();
    }
}
```
