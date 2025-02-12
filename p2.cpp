#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <limits>
#include <algorithm>

using namespace std;

// Represents a connection between stations
struct Edge {
    int to;
    int line;
};

// Function to calculate minimum line changes between two stations
int calculateMinLineChanges(const vector<vector<Edge>>& graph, int start, int end, int n) {
    vector<int> minChanges(n + 1, numeric_limits<int>::max());
    vector<int> currentLine(n + 1, -1);
    queue<int> q;
    
    // Initialize start station
    minChanges[start] = 0;
    q.push(start);
    
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        
        // Process all adjacent stations
        for (const Edge& edge : graph[current]) {
            int newChanges = minChanges[current];
            
            // If this is not the first station and we're changing lines, increment changes
            if (currentLine[current] != -1 && currentLine[current] != edge.line) {
                newChanges++;
            }
            
            // Update if we found a better path
            if (newChanges < minChanges[edge.to]) {
                minChanges[edge.to] = newChanges;
                currentLine[edge.to] = edge.line;
                q.push(edge.to);
            }
        }
    }
    
    return minChanges[end];
}

int main() {
    // Read input parameters
    int n, m, l;
    cin >> n >> m >> l;
    
    // Create adjacency list representation of the graph
    vector<vector<Edge>> graph(n + 1);
    
    // Read and store edges
    int line, x, y;
    while (cin >> line >> x >> y) {
        int line, x, y;
        cin >> line >> x >> y;
        graph[x].push_back({y, line});
        graph[y].push_back({x, line}); // Add reverse edge (undirected graph)
    }
    
    // Calculate maximum minimum line changes between any two stations
    int maxChanges = 0;
    bool hasDisconnectedStations = false;
    
    // Check connectivity and calculate maximum changes
    for (int i = 1; i <= n && !hasDisconnectedStations; i++) {
        for (int j = i + 1; j <= n; j++) {
            int changes = calculateMinLineChanges(graph, i, j, n);
            
            if (changes == numeric_limits<int>::max()) {
                hasDisconnectedStations = true;
                break;
            }
            
            maxChanges = max(maxChanges, changes);
        }
    }
    
    // Output result
    if (hasDisconnectedStations) {
        cout << -1;
    } else {
        cout << maxChanges-1;
    }
    
    return 0;
}
