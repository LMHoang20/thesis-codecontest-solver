import sys
import subprocess
import unicodedata
file_name = sys.argv[1]

result = ""

with open(file_name, 'r') as f:
    result = f.read()
    result = result.replace('—', '-')
    result = result.replace('& mdash;', '-')
    result = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore').decode('utf-8')
    result = result.replace('# include', '#include')
    result = result.replace('__gcd', 'gcd')
    result = result.replace('return (cin', 'return bool(cin')
    result = result.replace('conj[', 'adj[')
    if '#define int ' in result:
        result = result.replace('\nmain(', '\nint32_t main(')
    else:
        result = result.replace('\nmain(', '\nint main(')
    if '3.14' in result:
        pi_position = result.find('3.14')
        next_semicolon = result.find(';', pi_position)
        if next_semicolon == -1:
            next_semicolon = len(result)
        next_comma = result.find(',', pi_position)
        if next_comma == -1:
            next_comma = len(result)
        next_newline = result.find('\n', pi_position)
        if next_newline == -1:
            next_newline = len(result)
        result = result[:pi_position] + 'acos(-1)' + result[min(
            next_semicolon, next_comma, next_newline
        ):]

last_include = result.rfind("#include")
last_include += result[last_include:].find("\n")

includes = result[:last_include]
includes = includes.split("\n")
new_includes = []
for include in includes:
    if include.startswith('//'):
        new_includes.append(include)
new_includes.append("#include <bits/stdc++.h>")
includes = "\n".join(new_includes)
rest = result[last_include:].replace('assert', 'static_assert')
result = includes + "\nint end_includes;\n" + rest
with open(file_name, 'w') as f:
    f.write(result)

preprocessed = subprocess.run(["gcc", "-E", file_name],
                              capture_output=True,
                              text=True).stdout

end_includes = preprocessed.find("int end_includes;")

preprocessed = includes + "\n" + preprocessed[end_includes +
                                              len("int end_includes;"):]

if '/Library/Developer/CommandLineTools/' in preprocessed:
    print('clang error')
    exit(1)

preprocessed = preprocessed.replace('''template <class A, class B> ostream &operator<<(ostream &out, const pair<A, B> &p) { return out << "(" << p.first << ", " << p.second << ")"; }
template <class A> ostream &operator<<(ostream &out, const vector<A> &v) {
  out << "[";
  for (int i = int(0); i < int(int((v).size())); i++) {
    if (i) {
      out << ", ";
    }
    out << v[i];
  }
  return out << "]";
}''', '')

preprocessed = preprocessed.split("\n")

with open(file_name, 'w') as f:
    for line in preprocessed:
        line = line.rstrip().replace('_Static_assert', 'assert').replace('pair query(vector<int> nodes) {', 'pair<int, int> query(vector<int> nodes) {')
        if line == "":
            continue
        if line[0] == '#' and line.find('#include') == -1:
            continue
        if line.find('tmp.cpp') != -1:
            continue
        if line.find('"<built-in>"') != -1:
            continue
        result = line.replace('std::__1::__get_nullptr_t()', 'nullptr')
        f.write(result + '\n')

formatted = subprocess.run(["clang-format", file_name], capture_output=True, text=True).stdout

with open(file_name, 'w') as f:
    f.write(formatted)