from model import Gemini
import judge

meow = """You are a contestant in a programming contest. You need to refactor a code program into multiple functions and debugging them. Following the declarative/functional programming paradigm.

The refactored program must have this template, the declaration must be in the correct order so that the code compile and run correctly.

```cpp
struct Input {
    // Declare input variables here
};

struct Output {
    // Declare output variables here
};

Input read_input() {
    // Read input from standard input (e.g. cin) and return the input as a struct
}

void print_output(Output output) {
    // Print the output to standard output (e.g. cout)
}

Output solve(Input input) {
    // Solve the problem and return the output as a struct
    // Must read the correct input, call the smaller functions correctly in the correct order, and print the correct output to the problem
    // Can only declare variables, and call smaller/builtin/STL functions, for loops, no logic here
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    cout << fixed; cout.precision(9);
    int t = 1;
    #ifdef MULTIPLE_TEST_CASES
    cin >> t;
    #endif
    for(int _ = 0; _ < t; _++) {
        cout << "DEBUG: Test case " << _ << endl;
        auto inputs = read_input();
        auto outputs = solve(inputs);
        print_output(outputs);
    }
}
```

Constraints:
- If the program have multiple #include, replace all of them with `#include <bits/stdc++.h>`.
- The program must not have any global variables except for constants.
- The `solve` must only call smaller functions, DEBUG the inputs and outputs of those smaller functions.
- ABSOLUTELY NO logic should be written in the `solve` function.
- Each smaller function should have a clear purpose, meaningful name, must be less than 20 lines, follow single responsibility rule, must not have any side effect, meaning it should only interact with the parameters passed to it by value, NEVER reference.
- For debugging purposes, before any function calls in the `solve` function, the inputs and outputs of these smaller functions should be written to the stdout as a variable declaration.
    - The name of the function should be written to the stdout. For example adding `cout << "DEBUG: Function " << <function_name>;` before the function call.
    - The input of the function should be written to the stdout as a variable declaration, in the order they are passed to the function. For example, adding `cout << "DEBUG: Input-Start\\n" << "int a = " << a << ";\\nInput-End";` before the function call.
    - The output of the function should be written to the stdout as a variable declaration, in the order they are returned from the function. For example, adding `cout << "DEBUG: Output-Start\\n" << "int a = " << a << ";\\nOutput-End";` after the function call.
- The solve function must be broken down to at least 1 smaller function.

The program to be refactored is as follows:
"""

prompt = """
Rewrite this program in Golang. Following declarative/functional programming paradigm.

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <utility>
#include <algorithm>
#include <string>
#include <set>
#include <stdio.h>
#include <sstream>
#include <math.h>


using namespace std;

int main() {
    cout << fixed;
    cout.precision(9);
    string s;
    cin >> s;
    int res = 0;
    int n = s.length();
    for (int i = 0; i < s.length(); i++) for (int j = i+1; j < s.length(); j++) {
        int ch = 0;
        for (int k = 0; j+k < n && s[i+k] == s[j+k]; k++) {
            ch++;
        }
        res = max(ch, res);
    }
    cout << res << endl;
    return 0;
}
```

Answer:

```go
"""

model = Gemini()

response = model.generate_content(prompt)

print(response.text)

# code = response.text[:response.text.find('```')].strip()

# with open(judge.code_file, 'w') as f:
    # f.write(code)

# print(judge.judge_compile())