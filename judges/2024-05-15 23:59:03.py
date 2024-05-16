def solve(s):
    # Check if the number of 'A's and 'B's is equal, and the number of 'B's and 'C's is equal.
    a_count = s.count('A')
    b_count = s.count('B')
    c_count = s.count('C')
    if a_count != b_count or b_count != c_count:
        return "NO"

    # Use a greedy algorithm to determine if it is possible to erase all the letters from the string.
    while s:
        # If the number of 'A's and 'B's is equal, erase one 'A' and one 'B' from the string.
        if a_count == b_count:
            s = s.replace('A', '', 1)
            s = s.replace('B', '', 1)
            a_count -= 1
            b_count -= 1
        # Otherwise, erase one 'B' and one 'C' from the string.
        else:
            s = s.replace('B', '', 1)
            s = s.replace('C', '', 1)
            b_count -= 1
            c_count -= 1

    # If the string is empty after the greedy algorithm has finished, return "YES".
    if not s:
        return "YES"

    # Otherwise, return "NO".
    return "NO"

if __name__ == "__main__":
    # Read the number of test cases.
    t = int(input())

    # Iterate over the test cases.
    for _ in range(t):
        # Read the string.
        s = input()

        # Solve the test case.
        result = solve(s)

        # Print the result.
        print(result)
