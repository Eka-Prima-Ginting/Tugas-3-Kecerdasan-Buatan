import heapq

def greedy_search(graph, heuristics, start, goal):
    """
    Greedy Search implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    if start == goal:
        return [start]

    priority_queue = [(heuristics[start], start)]
    visited = set()
    parent = {start: None}

    print(f"Starting Greedy Search from {start} to {goal}")
    print(f"Heuristics: {heuristics}")
    print(f"Initial priority queue: {priority_queue}")
    print()

    while priority_queue:
        current_heuristic, current = heapq.heappop(priority_queue)
        print(f"Popped: {current} (heuristic: {current_heuristic})")

        if current in visited:
            print(f"Already visited {current}, skipping")
            continue

        visited.add(current)
        print(f"Visiting: {current}")

        if current == goal:
            print(f"Goal {goal} reached!")
            return reconstruct_path(parent, goal)

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (heuristics[neighbor], neighbor))
                parent[neighbor] = current
                print(f"Pushed neighbor: {neighbor} (heuristic: {heuristics[neighbor]})")

        print(f"Priority queue now: {priority_queue}")
        print("---")

    print("No path found")
    return None

def reconstruct_path(parent, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# Example usage
if __name__ == "__main__":
    # Graph: A -> B, C; B -> D; C -> E; D -> E
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': ['E'],
        'E': []
    }

    # Heuristics (e.g., straight-line distance to E)
    heuristics = {
        'A': 3,
        'B': 2,
        'C': 1,
        'D': 1,
        'E': 0
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print()

    path = greedy_search(graph, heuristics, 'A', 'E')
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
