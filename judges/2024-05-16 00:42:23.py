import sys

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def solve(a):
    a.sort()
    max_size = 0
    max_subset = []
    current_subset = []
    current_sum = 0
    for x in a:
        if current_sum + x > 1 and is_prime(current_sum + x):
            break
        current_subset.append(x)
        current_sum += x
    if len(current_subset) > max_size:
        max_size = len(current_subset)
        max_subset = current_subset
    return max_size, max_subset

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        max_size, max_subset = solve(a)
        print(max_size)
        print(*max_subset)

if __name__ == "__main__":
    main()
