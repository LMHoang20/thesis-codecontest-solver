def count_permutations(n):
  # Define the dynamic programming table.
  dp = [[0 for _ in range(n+1)] for _ in range(n+1)]

  # Initialize the dynamic programming table.
  dp[0][0] = 1
  for i in range(1, n+1):
    for j in range(1, n+1):
      for k in range(1, j):
        dp[i][j] += dp[i-1][k]

  # Answer the query.
  return dp[n][n]
