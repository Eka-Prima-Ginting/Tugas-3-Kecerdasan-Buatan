import heapq

def dijkstra(graph, start):
    """
    Dijkstra's algorithm implementation with simulation.

    Args:
    graph (dict): Adjacency list with weights, e.g., {'A': [('B', 1), ('C', 4)]}
    start: Starting node.

    Returns:
    dict: Shortest distances from start to all nodes.
    dict: Previous nodes for path reconstruction.
    """
    # Priority queue: (distance, node)
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    print(f"Starting Dijkstra from node: {start}")
    print(f"Initial distances: {distances}")
    print(f"Initial priority queue: {pq}")
    print()

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        print(f"Popped: {current_node} with distance {current_distance}")

        if current_distance > distances[current_node]:
            print(f"Skipping {current_node} as better path found")
            continue

        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                print(f"Updated distance for {neighbor} to {distance} via {current_node}")
                print(f"Priority queue now: {pq}")
                print(f"Distances now: {distances}")
        print("---")

    print(f"\nFinal shortest distances: {distances}")
    return distances, previous

# Example usage
if __name__ == "__main__":
    # Weighted graph: A -> B(1), C(4); B -> C(2), D(5); C -> D(1)
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }

    print("Graph adjacency list with weights:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print()

    dijkstra(graph, 'A')
