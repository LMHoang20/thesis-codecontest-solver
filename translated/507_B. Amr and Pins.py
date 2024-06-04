r, x, y, xx, yy = map(int, input().split())

r *= 2
dist = (x - xx) ** 2 + (y - yy) ** 2
r *= r

L, R = 0, 1000000
while R > L:
    mid = L + (R - L) // 2
    temp = mid * mid * r
    if temp >= dist:
        R = mid
    else:
        L = mid + 1

print(R)