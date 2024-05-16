import sys

def main():
    # Read the number of test cases
    t = int(input())

    # Iterate over the test cases
    for i in range(t):
        # Read the number of one-minute, two-minute, and three-minute songs
        a, b, c = map(int, input().split())

        # Find the total duration of all the songs
        total_duration = a + 2 * b + 3 * c

        # Find the minimum possible difference in durations
        min_difference = min(total_duration - a, total_duration - (a + 2 * b))

        # Print the minimum possible difference in durations
        print(min_difference)

if __name__ == "__main__":
    main()
