## Name

A: 14_A. Letter

## Description

A boy Bob likes to draw. Not long ago he bought a rectangular graph (checked) sheet with n rows and m columns. Bob shaded some of the squares on the sheet. Having seen his masterpiece, he decided to share it with his elder brother, who lives in Flatland. Now Bob has to send his picture by post, but because of the world economic crisis and high oil prices, he wants to send his creation, but to spend as little money as possible. For each sent square of paper (no matter whether it is shaded or not) Bob has to pay 3.14 burles. Please, help Bob cut out of his masterpiece a rectangle of the minimum cost, that will contain all the shaded squares. The rectangle's sides should be parallel to the sheet's sides.

Input

The first line of the input data contains numbers n and m (1 ≤ n, m ≤ 50), n — amount of lines, and m — amount of columns on Bob's sheet. The following n lines contain m characters each. Character «.» stands for a non-shaded square on the sheet, and «*» — for a shaded square. It is guaranteed that Bob has shaded at least one square.

Output

Output the required rectangle of the minimum cost. Study the output data in the sample tests to understand the output format better.

Examples

Input

6 7
.......
..***..
..*....
..***..
..*....
..***..


Output

***
*..
***
*..
***


Input

3 3
***
*.*
***


Output

***
*.*
***

## Editorial

To find the smallest rectangle containing the picture, iterate through the pairs $(i,j)$ such that the $j-th$ symbol in $i-th$ line is '*'; find the minimum and maximum values of $i$ and $j$ from these pairs. The rectangle to output is $[i_{min}, i_{max}] × [j_{min}, j_{max}]$.

## Code

```cpp
#include<bits/stdc++.h>
using namespace std;
int n,m,p,q,x,y;
char g,a[101][101];
int main(){
	scanf("%d%d",&n,&m);
	p=100000,x=100000;
	for(int i=1;i<=n;i++)
		for(int j=1;j<=m;j++){
			cin>>g;
			a[i][j]=g;
			if(g=='*'){
				if(i<=p) p=i;
				if(j<=x) x=j;
				if(i>=q) q=i;
				if(j>=y) y=j;
			}
		}
	for(int i=p;i<=q;i++){
		for(int j=x;j<=y;j++)
			printf("%c",a[i][j]);
	    cout<<'\n';
	}
	return 0;
}
```

# Answer

Incorrect code:

```cpp
#include<bits/stdc++.h>
using namespace std;

// input function
pair<int, int> read_inputs() {
    int n, m;
    cin >> n >> m;
    return {n, m};
}

// read and process input data
vector<string> read_data(int n, int m) {
    vector<string> data(n);
    for (int i = 0; i < n; i++) {
        string line;
        cin >> line;
        data[i] = line;
    }
    return data;
}

// search for the top left and bottom right coordinates of the minimal rectangle
pair<pair<int, int>, pair<int, int>> search_coordinates(const vector<string>& data) {
    int p = data.size(), x = data[0].size();
    for (int i = 0; i < data.size(); i++) {
        for (int j = 0; j < data[i].size(); j++) {
            if (data[i][j] == '*') {
                if (i < p) p = i;
                if (j < x) x = j;
                if (i > q) q = i;
                if (j > y) y = j;
            }
        }
    }
    return { {p, x}, {q, y} };
}

// print the minimal rectangle
void print_rectangle(const vector<string>& data, pair<pair<int, int>, pair<int, int>> coords) {
    for (int i = coords.first.first; i <= coords.second.first; i++) {
        for (int j = coords.first.second; j <= coords.second.second; j++)
            cout << data[i][j];
        cout << '\n';
    }
}

int main() {
    auto [n, m] = read_inputs();
    auto data = read_data(n, m);
    auto coords = search_coordinates(data);
    print_rectangle(data, coords);
}
```

# Compiler Output

tmp.cpp:30:25: error: use of undeclared identifier 'q'
                if (i > q) q = i;
                        ^
tmp.cpp:30:28: error: use of undeclared identifier 'q'
                if (i > q) q = i;
                           ^
tmp.cpp:31:25: error: use of undeclared identifier 'y'
                if (j > y) y = j;
                        ^
tmp.cpp:31:28: error: use of undeclared identifier 'y'
                if (j > y) y = j;
                           ^
tmp.cpp:35:23: error: use of undeclared identifier 'q'
    return { {p, x}, {q, y} };
                      ^
tmp.cpp:35:26: error: use of undeclared identifier 'y'
    return { {p, x}, {q, y} };
                         ^

# Answer

Correct code:

```cpp
#include<bits/stdc++.h>
using namespace std;

// input function
pair<int, int> read_inputs() {
    int n, m;
    cin >> n >> m;
    return {n, m};
}

// read and process input data
vector<string> read_data(int n, int m) {
    vector<string> data(n);
    for (int i = 0; i < n; i++) {
        string line;
        cin >> line;
        data[i] = line;
    }
    return data;
}

// search for the top left and bottom right coordinates of the minimal rectangle
pair<pair<int, int>, pair<int, int>> search_coordinates(const vector<string>& data) {
    int p = data.size(), x = data[0].size();
    int q = -1, y = -1;
    for (int i = 0; i < data.size(); i++) {
        for (int j = 0; j < data[i].size(); j++) {
            if (data[i][j] == '*') {
                if (i < p) p = i;
                if (j < x) x = j;
                if (i > q) q = i;
                if (j > y) y = j;
            }
        }
    }
    return { {p, x}, {q, y} };
}

// print the minimal rectangle
void print_rectangle(const vector<string>& data, pair<pair<int, int>, pair<int, int>> coords) {
    for (int i = coords.first.first; i <= coords.second.first; i++) {
        for (int j = coords.first.second; j <= coords.second.second; j++)
            cout << data[i][j];
        cout << '\n';
    }
}

int main() {
    auto [n, m] = read_inputs();
    auto data = read_data(n, m);
    auto coords = search_coordinates(data);
    print_rectangle(data, coords);
}
```

# Compiler Output

OK
