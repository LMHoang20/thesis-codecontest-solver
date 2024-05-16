def is_fair_playoff(t):
    for _ in range(t):
        # Read the skill levels of the four players
        s = list(map(int, input().split()))
        # Sort the skill levels
        s.sort(reverse=True)
        # The top two players in the finals
        finalists = s[:2]
        # Check if the top two players are the highest in the initial set
        if finalists == s[:2]:
            print("YES")
        else:
            print("NO")

# Read the number of test cases
t = int(input())
is_fair_playoff(t)