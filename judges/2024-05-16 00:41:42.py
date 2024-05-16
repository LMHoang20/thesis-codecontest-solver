t = int(input())
for _ in range(t):
    s = input()
    a = s.count('A')
    b = s.count('B')
    c = s.count('C')
    if a == b and b == c:
        if a == 0:
            print("YES")
        else:
            print("NO")
    else:
        print("NO")
