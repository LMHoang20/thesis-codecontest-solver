#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

typedef pair<int, int> pii;  // (day, lake) for observations

// Calculate distances from a reference lake (lake 1)
void calculateDistances(vector<vector<pii>>& adjList, vector<int>& dist) {
    queue<int> q;
    q.push(1); // Reference lake
    dist[1] = 0;

    while (!q.empty()) {
        int currLake = q.front(); q.pop();
        for (pii neighbor : adjList[currLake]) {
            int nextLake = neighbor.first;
            int edgeLen = neighbor.second;
            if (dist[nextLake] == -1) { // Unvisited
                dist[nextLake] = dist[currLake] + edgeLen;
                q.push(nextLake);
            }
        }
    }
}

int main() {
    int n, k;
    cin >> n; // Number of lakes

    // Adjacency list for graph representation
    vector<vector<pii>> adjList(n + 1); 
    for (int i = 0; i < n - 1; ++i) {
        int u, v, l;
        cin >> u >> v >> l;
        adjList[u].push_back({v, l});
        adjList[v].push_back({u, l});
    }

    vector<int> dist(n + 1, -1); // Distances from lake 1
    calculateDistances(adjList, dist);

    cin >> k; // Number of observations
    vector<vector<pii>> observations(n + 1);
    for (int i = 0; i < k; ++i) {
        int d, f, p;
        cin >> d >> f >> p;
        observations[p].push_back({d, f});
    }

    int totalFish = 0;

    // Process observations for each lake
    for (int lake = 1; lake <= n; ++lake) {
        sort(observations[lake].begin(), observations[lake].end());

        priority_queue<pii, vector<pii>, greater<pii>> activeWindows; // Min-heap
        for (pii obs : observations[lake]) {
            int day = obs.first;
            int fish = obs.second;

            // Remove expired windows
            while (!activeWindows.empty() && activeWindows.top().first < day - dist[lake]) {
                activeWindows.pop();
            }

            // Overlap: extend existing window
            if (!activeWindows.empty()) {
              int top = activeWindows.top().second;
              top += fish; 
              activeWindows.pop();
              activeWindows.push({day, top});
            } 
            // No overlap: add new window
            else {
                activeWindows.push(obs);
            }
        }
        totalFish += activeWindows.size(); // Fish needed for this lake
    }

    cout << totalFish << endl;
    return 0;
}
