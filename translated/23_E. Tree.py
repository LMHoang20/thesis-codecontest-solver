import sys
from functools import cmp_to_key
from collections import defaultdict
from math import gcd

sys.setrecursionlimit(10000)

n = 0
f = [1] * 800
h = [1] * 800
children = defaultdict(list)

def compare(i1, i2):
    if f[i2] * h[i1] > f[i1] * h[i2]:
        return 1
    elif f[i2] * h[i1] < f[i1] * h[i2]:
        return -1
    else:
        return 0

def rec(v, parent):
    if parent in children[v]:
        children[v].remove(parent)
    
    f[v] = 1
    has_leaves = False
    for u in children[v]:
        rec(u, v)
        if h[u] == 1:
            has_leaves = True
        else:
            f[v] *= h[u]
    
    children[v].sort(key=cmp_to_key(compare))
    h[v] = f[v]
    
    cur = f[v]
    for k, u in enumerate(children[v]):
        cur = cur // h[u] * f[u]
        ch = cur * (k + 2)
        if ch > h[v]:
            h[v] = ch
    
    if not has_leaves:
        for w in children[v]:
            cur = f[v] // h[w] * f[w]
            for k, u in enumerate(children[w]):
                cur = cur // h[u] * f[u]
                ch = cur * (k + 3)
                if ch > h[v]:
                    h[v] = ch

if __name__ == "__main__": 
    n = int(input())
    idx = 1
    for i in range(n):
        children[i] = []
    for i in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        idx += 2
        children[a].append(b)
        children[b].append(a)
    
    rec(0, -1)
    
    print(h[0])
