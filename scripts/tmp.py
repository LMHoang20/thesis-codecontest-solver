def reach_cell(n, m, k):
  """
  This function checks if it's possible to reach cell (n, m) spending exactly k burles.

  Args:
      n: Grid size in n direction.
      m: Grid size in m direction.
      k: Target cost to spend.

  Returns:
      "YES" if reachable with exact cost, "NO" otherwise.
  """
  # Create dp table with size n+1 (for base case) x m+1
  dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]

  # Base Case - starting cell has no cost
  dp[1][1] = 0

  # Fill the dp table
  for i in range(1, n + 1):
    for j in range(1, m + 1):
      # Minimum cost from left or top cell + corresponding move cost
      if i == 1 and j == 1:
        continue
      dp[i][j] = min(dp[i][j - 1] + j, dp[i - 1][j] + i)
  # Check if reachable with exact cost
  return "YES" if dp[n][m] == k else "NO"

# Read the number of test cases
t = int(input())

for _ in range(t):
  # Read input for each test case
  n, m, k = map(int, input().split())
  # Call the function and print result
  print(reach_cell(n, m, k))
