def main():
    n = int(input())
    table = [[1 for _ in range(n)] for _ in range(n)]

    for i in range(1, n):
        for j in range(1, n):
            table[i][j] = table[i - 1][j] + table[i][j - 1]

    max_value = table[n - 1][n - 1]
    print(max_value)

if __name__ == "__main__":
    main()