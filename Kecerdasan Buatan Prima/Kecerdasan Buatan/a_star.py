import heapq

def a_star_search(graph, weights, heuristics, start, goal):
    """
    A* Search implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    weights (dict): Weights for edges, e.g., {(u,v): weight}.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    if start == goal:
        return [start]

    priority_queue = [(heuristics[start], 0, start)]  # (f, g, node)
    g_cost = {start: 0}
    parent = {start: None}

    print(f"Starting A* Search from {start} to {goal}")
    print(f"Heuristics: {heuristics}")
    print(f"Initial priority queue: {priority_queue}")
    print()

    while priority_queue:
        f, g, current = heapq.heappop(priority_queue)
        print(f"Popped: {current} (f: {f}, g: {g}, h: {heuristics[current]})")

        if current == goal:
            print(f"Goal {goal} reached!")
            return reconstruct_path(parent, goal)

        for neighbor in graph.get(current, []):
            edge_weight = weights.get((current, neighbor), 1)  # Default weight 1
            new_g = g + edge_weight
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_new = new_g + heuristics[neighbor]
                heapq.heappush(priority_queue, (f_new, new_g, neighbor))
                parent[neighbor] = current
                print(f"Updated neighbor: {neighbor} (g: {new_g}, h: {heuristics[neighbor]}, f: {f_new})")

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
    # Graph: A -> B(1), C(4); B -> D(2); C -> E(3); D -> E(1)
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': ['E'],
        'E': []
    }

    # Weights
    weights = {
        ('A', 'B'): 1,
        ('A', 'C'): 4,
        ('B', 'D'): 2,
        ('C', 'E'): 3,
        ('D', 'E'): 1
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
    print("Weights:")
    for edge, weight in weights.items():
        print(f"{edge}: {weight}")
    print()

    path = a_star_search(graph, weights, heuristics, 'A', 'E')
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
