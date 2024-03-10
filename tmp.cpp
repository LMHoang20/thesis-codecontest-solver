#include <iostream>
#include <limits>

using namespace std;

int main() {
  int t;

  // Get the total number of test cases
  cout << "Enter the number of test cases: ";
  cin >> t;

  for (int i = 0; i < t; ++i) {
    int n;

    // Get the size of the array for the current test case
    cout << "Enter the size of the array for test case " << i + 1 << ": ";
    cin >> n;

    int a[n]; // Array to store input numbers
    int count_negative = 0, count_zero = 0, count_positive = 0;

    // Read elements of the array
    cout << "Enter elements of the array (space-separated): ";
    for (int j = 0; j < n; ++j) {
      cin >> a[j];

      if (a[j] < 0) {
        count_negative++;
      } else if (a[j] == 0) {
        count_zero++;
      } else {
        count_positive++;
      }
    }

    // Determine minimum operations
    int min_operations = 0;
    if (count_zero > 0 || count_negative % 2 != 0) {
      // No operations needed if there's a zero or odd negative numbers
      min_operations = 0;
    } else if (count_positive > 0) {
      // One operation needed if only positive numbers and even negatives
      min_operations = 1;
    }

    // Output
    cout << "Test Case " << i + 1 << ":" << endl;
    cout << "Minimum operations needed: " << min_operations << endl;

    // Print instructions for one operation (if applicable)
    if (min_operations == 1) {
      int index_to_change = 0; // Assuming we can change the first element

      cout << "Operation: Change element at index " << index_to_change << " to 0." << endl;
    }

    cout << endl;
  }

  return 0;
}
