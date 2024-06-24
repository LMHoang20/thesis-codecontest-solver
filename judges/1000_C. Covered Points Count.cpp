#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    // Store the segments as pairs of endpoints
    vector<pair<long long, long long>> segments(n);
    for (int i = 0; i < n; ++i) {
        cin >> segments[i].first >> segments[i].second;
    }
    
    // Create a vector to store all unique endpoints
    vector<long long> uniqueEndpoints;
    for (auto& segment : segments) {
        uniqueEndpoints.push_back(segment.first);
        uniqueEndpoints.push_back(segment.second + 1);
    }
    
    // Sort and remove duplicates from the vector of unique endpoints
    sort(uniqueEndpoints.begin(), uniqueEndpoints.end());
    uniqueEndpoints.resize(unique(uniqueEndpoints.begin(), uniqueEndpoints.end()) - uniqueEndpoints.begin());
    
    // Create a vector to store the count of segments covering each point
    vector<int> segmentCounts(uniqueEndpoints.size());
    
    // Iterate through each segment and update the count vector
    for (auto& segment : segments) {
        // Find the indices of the endpoints in the uniqueEndpoints vector
        int leftIndex = lower_bound(uniqueEndpoints.begin(), uniqueEndpoints.end(), segment.first) - uniqueEndpoints.begin();
        int rightIndex = lower_bound(uniqueEndpoints.begin(), uniqueEndpoints.end(), segment.second + 1) - uniqueEndpoints.begin();
        
        // Increment the count at the left endpoint and decrement at the right endpoint
        segmentCounts[leftIndex]++;
        segmentCounts[rightIndex]--;
    }
    
    // Calculate the prefix sums of the count vector
    for (int i = 1; i < segmentCounts.size(); ++i) {
        segmentCounts[i] += segmentCounts[i - 1];
    }
    
    // Create a vector to store the final answer
    vector<long long> answer(n + 1);
    
    // Iterate through the count vector and calculate the answer
    for (int i = 1; i < segmentCounts.size(); ++i) {
        // Calculate the number of points covered by the current number of segments
        answer[segmentCounts[i - 1]] += uniqueEndpoints[i] - uniqueEndpoints[i - 1];
    }
    
    // Print the answer
    for (int i = 1; i <= n; ++i) {
        cout << answer[i] << " ";
    }
    cout << endl;
    
    return 0;
}

